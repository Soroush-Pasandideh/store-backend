from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)

        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk'].count() > 0):
            return Response({'error': 'product cannot be deleted because it is associated with an order item.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'product cannot be deleted because it is associated with an order item.'},
    #                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=HTTP_204_NO_CONTENT)


# class ProductList(ListCreateAPIView):
# --------------------
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}
# ---------------------
# using the above implementation we don't need following methods anymore
# def get(self, request):
#     queryset = Product.objects.select_related('collection').all()
#     serializer = ProductSerializer(queryset, many=True, context={'request': request})
#     return Response(serializer.data)
#
# def post(self, request):
#     serializer = ProductSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=HTTP_201_CREATED)
# --------------------------

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'product cannot be deleted because it is associated with an order item.'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk'].count() > 0):
            return Response({'error': 'Collection cannot be deleted because it has more than one products'})
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'Collection cannot be deleted because it has more than one products'})
    #     collection.delete()
    #     return Response(status=HTTP_204_NO_CONTENT)


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products'))
#     serializer_class = CollectionSerializer
#
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it has more than one products'})
#         collection.delete()
#         return Response(status=HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
