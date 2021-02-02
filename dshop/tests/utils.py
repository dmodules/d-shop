import requests
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

def product_brand():
    brand, created = ProductBrand.objects.get_or_create(
        name='D-Mart',
        logo=get_image(),
        order=1)
    return brand

def category():
    cat, created = ProductCategory.objects.get_or_create(name='Vegetable')
    return cat

def attribute():
    attr, created = Attribute.objects.get_or_create(name='KG')
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
