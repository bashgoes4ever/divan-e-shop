from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import *


class Misc(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        contacts = Contacts.objects.all()[0]
        contacts_serializer = ContactsSerializer(contacts, many=False)
        slider = Slide.objects.all().order_by('-priority')
        slider_serializer = SliderSerializer(slider, many=True)
        return Response({
            "contacts": contacts_serializer.data,
            "slider": slider_serializer.data
        })