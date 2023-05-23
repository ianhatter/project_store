from rest_framework import serializers
from Products.models import Products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'Product_name', 'Product_SKU', 'description',
                  'published')
