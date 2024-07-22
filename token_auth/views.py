# views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserLogoutSerializer, TodoItemSerializer
from rest_framework.permissions import IsAuthenticated
from .models import TodoItem

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({'username': user.username, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'username': user.username, 'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        serializer = UserLogoutSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                token = Token.objects.get(user=user)
                token.delete()
                return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
            except (User.DoesNotExist, Token.DoesNotExist):
                return Response({'error': 'Invalid username or token not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoItemListCreateView(generics.ListCreateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [IsAuthenticated]