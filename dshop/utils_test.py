from dshop.models import ProductDefault, ProductCategory, ProductFilter


def filter_p():
    filt = ProductFilter.objects.create(name='ALL')
    return filt

def category():
    cat, created = ProductCategory.objects.get_or_create(name='Vegetable')
    return cat

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
