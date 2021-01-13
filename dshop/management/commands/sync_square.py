
from django.core.management.base import BaseCommand
import json
from dshop.models import ProductCategory
from dshop.models import Attribute, AttributeValue
from dshop.models import ProductVariable, ProductVariableVariant

from square.client import Client

token = 'EAAAEJN_OPH4v-cyNo4E2nNmpCg1QlL4BFuwQbLYlRnZ1h-8I2WXyNOkCE81mBv2'

client = Client(
    access_token=token,
    environment='production',
)

class Command(BaseCommand):

    def handle(self, **options): # noqa

        result = client.catalog.list_catalog()
        data = result.body
        #data = json.loads(data)

        #Create Category
        for d in data['objects']:
            if d['type'] == 'CATEGORY':
                cat_data = {
                    'name': d['category_data']['name'],
                    'square_id': d['id']
                }
                ProductCategory.objects.get_or_create(**cat_data)

        #Create Attribute and its value
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
                    attr_val_obj = AttributeValue.objects.get_or_create(**attr_value)

        for d in data['objects']:
            if d['type'] == 'ITEM':
                if 'category_id' in d['item_data']:
                    cat = ProductCategory.objects.get(square_id=d['item_data']['category_id'])
                    print(cat)
                    print("==== " +d['item_data']['name'])
                else:
                    print("--" +d['item_data']['name'])
                p_data = {
                    'product_name': d['item_data']['name'],
                    'order': 1 
                }
                product_variable, created = ProductVariable.objects.get_or_create(**p_data)
                product_variable.description = d['item_data']['description']
                try:
                    cat = d['item_data']['category_id']
                    cat_obj = ProductCategory.objects.get(square_id=cat)
                    product_variable.categories.add(cat_obj)
                except Exception as e:
                    print(e)
                #Create variants 
                for vari in d['item_data']['variations']:
                    print(vari)
                    result = client.inventory.retrieve_inventory_count(catalog_object_id=vari['id'])
                    r_body = result.body
                    product_code = vari['id']
                    quantity = 0
                    try:
                        price = vari['item_variation_data']['price_money']['amount']
                    except Exception as e:
                        print(e)
                        price = 0
                    if r_body:
                        quantity = r_body['counts'][0]['quantity']
                    pv_data = {
                        'product': product_variable,
                        'product_code': product_code,
                        'unit_price': price,
                        'discounted_price': price,
                        'quantity': quantity
                    }
                    pvv, created = ProductVariableVariant.objects.get_or_create(**pv_data)

                    try:
                        for value_id in vari['item_variation_data']['item_option_values']:
                            attribute_value_id = value_id['item_option_value_id']
                            attribute_value_obj = AttributeValue.objects.get(square_id=attribute_value_id)
                            pvv.attribute.add(attribute_value_obj)
                    except Exception as e:
                        print(e)

                #Remove Variants
                existing_var = product_variable.variants.all().count()
                from_square_var = len(d['item_data']['variations'])
                from_square_var_id = [ v['id'] for v in d['item_data']['variations']]
                if existing_var > from_square_var:
                    for pv in product_variable.variants.all():
                        print(pv.product_code)
                        if not pv.product_code in from_square_var_id:
                            print('delete product..')
                        
