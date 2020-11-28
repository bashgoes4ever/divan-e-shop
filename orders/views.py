from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *
from rest_framework import status
from basket.models import Basket


class OrderView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # save order
        serializer = OrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # save products in order
        session_key = request.META['HTTP_AUTHORIZATION']
        basket = Basket.objects.get(user=session_key)
        products = basket.products.all()
        for product in products:
            ProductInOrder.objects.create(
                order=order,
                product=product.product,
                quantity=product.quantity,
                color=product.color,
                casing=product.casing,
            )
        return Response(status=status.HTTP_201_CREATED)