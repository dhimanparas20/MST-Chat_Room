from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserDetail, Group, GroupMessage
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token  # Correct import
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

#when sending token in header we nedd to specify Toekn or Bearer
# use [BearerTokenAuthentication] insted of [TokenAuthentication]
class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

#Return User details
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['id', 'username', 'email', 'first_name', 'last_name']
    filterset_fields = ['id', 'username', 'email']

class Home(APIView):
    def get(self, request):
        return render(request, 'home.html')

# Login for User
class Login(APIView):
    def get(self, request):
        return render(request, 'login.html')
    
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

#Logout
class Logout(APIView):
    def post(self, request, format=None):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token_key = auth_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                token.delete()
                return Response({'success': 'Successfully logged out'}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Authorization header missing or invalid'}, status=status.HTTP_400_BAD_REQUEST)