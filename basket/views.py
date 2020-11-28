from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *
from rest_framework import status


class ProductsInBasket(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ProductInBasketSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance_serializer = ProductInBasketViewSerializer(instance)
        return Response(
            instance_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, id=None):
        if ProductInBasket.objects.filter(id=id).exists():
            product = ProductInBasket.objects.get(id=id)
            serializer = ProductInBasketSerializer(product, data=request.data, many=False, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.update(product, request.data)
            return Response(
                {
                    'message': 'product updated'
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'message': 'product not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, id=None):
        session_key = request.META['HTTP_AUTHORIZATION']
        if ProductInBasket.objects.filter(id=id).exists():
            product = ProductInBasket.objects.get(id=id)
            if product.basket.user == session_key:
                product.delete()
                return Response(
                    {
                        'message': 'ProductInBasket deleted'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'message': 'You have no rights to edit this basket.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'message': 'ProductInBasket not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )


class BasketView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # if not request.session.exists(request.session.session_key):
        #     request.session.create()

        if 'HTTP_AUTHORIZATION' not in request.META:
            request.session.create()
            session_key = request.session.session_key
        else:
            session_key = request.META['HTTP_AUTHORIZATION']
        obj, created = Basket.objects.get_or_create(user=session_key)
        serializer = BasketSerializer(obj)
        return Response({
            'data': serializer.data,
            'session_key': session_key
        })