import re
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from filer.models import Image
from dshop.models import ProductCategory
from dshop.models import Attribute, AttributeValue
from dshop.models import ProductVariable, ProductVariableVariant

from settings import SQUARE_TOKEN, SQUARE_ENV
from square.client import Client


client = Client(
    access_token=SQUARE_TOKEN,
    environment=SQUARE_ENV,
)

class Command(BaseCommand):

    def handle(self, **options): # noqa

        if not SQUARE_TOKEN or not SQUARE_ENV:
            print("Plese add SQUARE_TOKEN and SQUARE_ENV variable in .env-local")
            return

        # Request for Categories
        result = client.catalog.list_catalog(types="category")
        if result.is_error():
            print("ERROR! " + str(result.errors))
            return
        data = result.body

        # Create Category
        print("Creating category...")
        for d in data['objects']:
            if d['type'] == 'CATEGORY':

                name = d['category_data']['name']
                name = name.replace('(', '<').replace(')','>')
                name = re.sub('<[^>]+>', '', name)
                cat_data = {
                    'name': name.strip(),
                    'square_id': d['id']
                }
                cat = ProductCategory.objects.filter(square_id=d['id'])
                if not cat:
                    ProductCategory.objects.create(**cat_data)
                else:
                    cat[0].name = name.strip()
                    cat[0].save()
        print("Created...")

        # Request for item_options (Attribute)
        result = client.catalog.list_catalog(types="item_option")
        if result.is_error():
            print("ERROR! " + str(result.errors))
            return
        data = result.body
        # Create Attribute and its value
        print("Creating attributes...")
        for d in data['objects']:
            if d['type'] == 'ITEM_OPTION':
                attr_data = {
                    'name': d['item_option_data']['name'],
                    'square_id': d['id']
                }
                attr_obj, created = Attribute.objects.get_or_create(**attr_data)
                for val in d['item_option_data']['values']:
                    attr_value = {
                        'attribute': attr_obj,
                        'value': val['item_option_value_data']['name'],
                        'square_id': val['id']
                    }
                    AttributeValue.objects.get_or_create(**attr_value)
        print("Created...")

        # Request for Image
        cursor = ''
        while True:
            result = client.catalog.list_catalog(
                types="image",
                cursor=cursor
            )
            if result.is_error():
                print("ERROR! " + str(result.errors))
                return
            data = result.body
            print("Creating an Image...")
            if 'objects' not in data:
                break
            for d in data['objects']:
                print('.', end=' ')
                if d['type'] == 'IMAGE':
                    name = d['id']
                    if 'url' in d['image_data']:
                        # if image is already there the skip!
                        if Image.objects.filter(name=name):
                            continue
                        url = d['image_data']['url']
                        try:
                            ext = url.rsplit('.',1)[1]
                            file_name = name + "." + ext
                        except Exception as e:
                            pass
                        r = requests.get(url)
                        image_temp_file = NamedTemporaryFile(delete=True)
                        image_temp_file.write(r.content)
                        image_temp_file.flush()
                        f = File(image_temp_file, name=file_name)
                        Image.objects.create(
                            original_filename=name,
                            file=f,
                            name=name
                        )
            if 'cursor' in data:
                print(data['cursor'])
                if cursor == data['cursor']:
                    print('No nexe page found')
                    break
                cursor = data['cursor']
                print('Next page')
            else:
                print('No nexe page found')
                break
        print("Created...")

        # Request for Item (Product)
        cursor = ''
        while True:
            result = client.catalog.list_catalog(
                types="item",
                cursor=cursor
            )
            if result.is_error():
                print("ERROR! " + str(result.errors))
                return
            data = result.body
            print("Creating Products...")
            for d in data['objects']:
                if d['type'] == 'ITEM':
                    if 'category_id' in d['item_data']:
                        cat = ProductCategory.objects.get(square_id=d['item_data']['category_id'])
                    description = ''
                    if 'description' in d['item_data']:
                        description = d['item_data']['description']
                    p_data = {
                        'product_name': d['item_data']['name'],
                        'square_id': d['id'],
                        'description': description,
                        'caption':description,
                        'order': 1
                    }
                    if ProductVariable.objects.filter(square_id=d['id']):
                        product_variable = ProductVariable.objects.get(square_id=d['id'])
                        product_variable.description = description
                        product_variable.caption = description
                    else:
                        product_variable = ProductVariable.objects.create(**p_data)

                    if 'image_id' in d:
                        img = Image.objects.filter(name=d['image_id'])
                        if img:
                            product_variable.main_image = img[0]
                            product_variable.save()

                    try:
                        cat = d['item_data']['category_id']
                        cat_obj = ProductCategory.objects.get(square_id=cat)
                        product_variable.categories.add(cat_obj)
                    except Exception as e:
                        print(e)
                    # Create variants
                    if 'variations' not in d['item_data']:
                        continue
                    for vari in d['item_data']['variations']:
                        result = client.inventory.retrieve_inventory_count(catalog_object_id=vari['id'])
                        r_body = result.body
                        product_code = vari['id']
                        quantity = 0
                        try:
                            price = vari['item_variation_data']['price_money']['amount']
                        except Exception:
                            print(vari['item_variation_data'])
                            price = 0
                        if r_body:
                            quantity = r_body['counts'][0]['quantity']
                        pv_data = {
                            'product': product_variable,
                            'product_code': product_code,
                            'unit_price': price/100,
                            'discounted_price': price/100,
                            'quantity': quantity
                        }
                        pvv = ProductVariableVariant.objects.filter(product_code=product_code)
                        if pvv:
                            pvv = pvv[0]
                            pvv.unit_price = price/100
                            pvv.quantity = quantity
                            pvv.save()
                        else:
                            pvv = ProductVariableVariant.objects.create(**pv_data)

                        if 'item_option_values' in vari['item_variation_data']:
                            for value_id in vari['item_variation_data']['item_option_values']:
                                attribute_value_id = value_id['item_option_value_id']
                                attribute_value_obj = AttributeValue.objects.get(square_id=attribute_value_id)
                                pvv.attribute.add(attribute_value_obj)

                    # Remove Variants
                    existing_var = product_variable.variants.all().count()
                    from_square_var = len(d['item_data']['variations'])
                    from_square_var_id = [v['id'] for v in d['item_data']['variations']]
                    if existing_var > from_square_var:
                        for pv in product_variable.variants.all():
                            print(pv.product_code)
                            if pv.product_code not in from_square_var_id:
                                print('delete product..')
            if 'cursor' in data:
                print(data['cursor'])
                if cursor == data['cursor']:
                    print('No nexe page found')
                    break
                cursor = data['cursor']
                print('Next page')
            else:
                print('No nexe page found')
                break
