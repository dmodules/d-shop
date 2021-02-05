import requests
import random
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from filer.models import Image

from dshop.models import ProductDefault, \
    ProductCategory, \
    ProductFilter, \
    ProductVariable, \
    ProductVariableVariant, \
    Attribute, \
    AttributeValue, \
    ProductBrand

def get_image():
    url = 'https://www.d-modules.com/static/img/logo-dmodules-black.png'
    r = requests.get(url)
    image_temp_file = NamedTemporaryFile(delete=True)
    image_temp_file.write(r.content)
    image_temp_file.flush()
    f = File(image_temp_file, name='test.png')
    img = Image.objects.create(
        original_filename='test',
        file=f,
        name='test'
    )
    return img


def filter_p():
    filt = ProductFilter.objects.create(name='ALL')
    return filt

def product_brand(data=None):
    if not data:
        data = {
            'name': 'D-Mart',
            'logo': get_image(),
            'order': 1
        }
    brand, created = ProductBrand.objects.get_or_create(**data)
    return brand

def category(data=None):
    if not data:
        data = {'name': 'Vegetable'}
    cat, created = ProductCategory.objects.get_or_create(**data)
    return cat

def attribute(name="KG"):
    attr, created = Attribute.objects.get_or_create(name=name)
    return attr

def attribute_value(attr, values=[1, 5]):
    value_list = []
    for val in values:
        attr_value, created = AttributeValue.objects.get_or_create(attribute=attr, value=val)
        value_list.append(attr_value)
    return value_list

def product(filter_p, category, data=None):

    try:
        if not data:
            data = {
                'product_name': 'Capsicum',
                'product_code': 'caps',
                'slug': 'capsicum',
                'unit_price': 100.00,
                'quantity': 100,
                'order': 0,
                'caption': 'Capsicum'
            }
        product = ProductDefault.objects.create(**data)

        if category:
            product.categories.add(category)
        if filter_p:
            product.filters.add(filter_p)
    except Exception as e:
        return type(e)

    return product

def product_variable(data=None):

    try:
        if not data:
            data = {
                'product_name': 'Capsicum',
                'slug': 'capsicum-123',
                'order': 0,
                'caption': 'Capsicum'
            }
        product = ProductVariable.objects.create(**data)
    except Exception as e:
        return type(e)
    return product

def product_variant(product, data=None):

    try:
        if not data:
            data = {
                'product': product,
                'product_code': '00001',
                'unit_price': 10,
                'quantity': 100,
            }
        product_variant = ProductVariableVariant.objects.create(**data)
    except Exception as e:
        return type(e)

    return product_variant

def attach_attribute(product_v, attribute):

    try:
        if not product_v or not attribute:
            return None

        product_v.attribute.add(attribute)
    except Exception as e:
        return type(e)

    return True

def clear_data():
    ProductVariable.objects.all().delete()
    ProductCategory.objects.all().delete()
    ProductBrand.objects.all().delete()
    Attribute.objects.all().delete()

def create_data():
    clear_data()
    for i in range(1, 5):
        data = {
            'name': 'Brand ' + str(i),
            'logo': get_image(),
            'order': i
        }
        product_brand(data)
        category({'name': "Category " + str(i)})

    for cat in ProductCategory.objects.all():
        data = {
            'parent': cat,
            'name': 'Child 1: ' + cat.name
        }
        category(data)
        data = {
            'parent': cat,
            'name': 'Child 2: ' + cat.name
        }
        category(data)

    attr = attribute('Color')
    attribute_value(attr, ['Red', 'Blue', 'Green'])
    attr = attribute('Size')
    attribute_value(attr, ['S', 'M', 'L', 'XL'])

    product_counter = 1
    b_counter = 0
    for cat in ProductCategory.objects.all().order_by('id'):
        brand = ProductBrand.objects.all().order_by('id')[b_counter]
        data = {
            'product_name': 'Product ' + str(product_counter),
            'order': product_counter,
            'brand': brand,
            'caption': 'Test Product ' + str(product_counter)
        }
        product = product_variable(data)
        price = random.randint(10, 50)
        quantity = random.randint(5, 25)
        data = {
            'product': product,
            'product_code': ''.join(random.sample('0123456789', 5)),
            'unit_price': price,
            'quantity': quantity,
        }
        product_variant(product, data)

        product.categories.add(cat)
        product_counter += 1

        data = {
            'product_name': 'Product ' + str(product_counter),
            'order': product_counter,
            'brand': brand,
            'caption': 'Test Product ' + str(product_counter)
        }
        product = product_variable(data)
        price = random.randint(10, 50)
        quantity = random.randint(5, 25)
        data = {
            'product': product,
            'product_code': ''.join(random.sample('0123456789', 5)),
            'unit_price': price,
            'quantity': quantity,
        }
        product_variant(product, data)

        product.categories.add(cat)
        product_counter += 1
        b_counter += 1
        if b_counter == 4:
            b_counter = 0
