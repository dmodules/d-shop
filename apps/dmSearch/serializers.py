from rest_framework import serializers
from dshop.models import Product, ProductCategory, ProductFilter


class ProductFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFilter
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    categories = ProductCategorySerializer(many=True, required=False)
    filters = ProductFilterSerializer(many=True, required=False)
    description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = (
            'cms_pages',
            'images',
            'polymorphic_ctype',
        )

    def get_caption(self, obj):
        return obj.get_caption

    def get_description(self, obj):
        return obj.get_description
