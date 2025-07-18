from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from accounts.serializers import UserSerializer


UserModel = get_user_model()

# Create your views here.
class RegisterView(CreateAPIView):
    queryset = UserModel.objects. all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

