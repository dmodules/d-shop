
from rest_framework import serializers
from dshop.models import Product, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
         model = ProductCategory
         field = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    categories = ProductCategorySerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

