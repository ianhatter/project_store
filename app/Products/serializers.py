from rest_framework import serializers
from Products.models import Products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'title', 'Products_url', 'image_path', 'description',
                  'published')
