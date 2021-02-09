from rest_framework import serializers
from .models import dmQuotation, dmQuotationItem


class dmQuotationItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = dmQuotationItem
        fields = '__all__'
        extra_kwargs = {
            'unit_price': {'read_only': True}
        }

class dmQuotationSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()

    class Meta:
        model = dmQuotation
        fields = ('id', 'number', 'status', 'created_at', 'updated_at', 'items')

    def get_items(self, obj):
        item_list = []
        for item in dmQuotationItem.objects.filter(quotation=obj):
            data = {
                'id': item.id,
                'product_name': item.product_name,
                'product_code': item.product_code,
                'variant_code': item.variant_code,
                'quantity': item.quantity
            }
            item_list.append(data)
        return {'items': item_list}
