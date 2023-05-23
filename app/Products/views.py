from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from Products.models import Products
from Products.serializers import ProductsSerializer
from rest_framework.decorators import api_view

# def index(request):
#     return render(request, "Products/index.html")


def index(request):
    print("Products are HERE")
    queryset = Products.objects.all()
    return render(request, "Products/index.html", {'Products': queryset})


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Products/index.html'

    def get(self, request):
        queryset = Products.objects.all()
        return Response({'Products': queryset})


class list_all_Products(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Products/Products_list.html'

    def get(self, request):
        queryset = Products.objects.all()
        return Response({'Products': queryset})


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def Products_list(request):
    if request.method == 'GET':
        Product = Products.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            Product = Products.filter(title__icontains=title)

        Products_serializer = ProductsSerializer(Product, many=True)
        return JsonResponse(Products_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        Products_data = JSONParser().parse(request)
        Products_serializer = ProductsSerializer(data=Products_data)
        if Products_serializer.is_valid():
            Products_serializer.save()
            return JsonResponse(Products_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(Products_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Products.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Product was deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def Products_detail(request, pk):
    try:
        Product = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        return JsonResponse({'message': 'The Product does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        Products_serializer = ProductsSerializer(Product)
        return JsonResponse(Products_serializer.data)

    elif request.method == 'PUT':
        Products_data = JSONParser().parse(request)
        Products_serializer = ProductsSerializer(Product, data=Products_data)
        if Products_serializer.is_valid():
            Products_serializer.save()
            return JsonResponse(Products_serializer.data)
        return JsonResponse(Products_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Product.delete()
        return JsonResponse({'message': 'Product was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def Products_list_published(request):
    Product = Products.objects.filter(published=True)

    if request.method == 'GET':
        Products_serializer = ProductsSerializer(Product, many=True)
        return JsonResponse(Products_serializer.data, safe=False)