from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import generics, authentication, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/sign_up.html'
    

    serializer_class = UserSerializer

    def get(self, request):
        serializer_class = UserSerializer
        return render(request, template_name = 'user/sign_up.html', context={'serializer_class': serializer_class})




class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):  # Method overide
        """Retrieve and return authenticated user"""
        return self.request.user



