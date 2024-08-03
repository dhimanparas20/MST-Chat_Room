from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserDetail, Group, GroupMessage, Conversation, Message
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token  # Correct import
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView

class Login(APIView):
    def post(self, request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)  # Serialize the user object
        return Response({
            "payload": serializer.data,
            "access": token.key  # Return the token key
        })
