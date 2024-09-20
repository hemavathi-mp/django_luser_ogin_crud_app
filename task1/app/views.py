from django.shortcuts import render, redirect

from rest_framework.generics import ListAPIView, RetrieveAPIView
from app.model import User
from app.serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib import messages


class LoginView(APIView):

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is not None and password is not None:
            data = User.objects.filter(name=username, password=password).all()
            if data.exists():
                return redirect('dashboard')  # Redirect to a dashboard or homepage
            else:
                return redirect('error')
      
        return render(request, 'login.html')

class DashboardView(APIView):
    def get(self, request):
        return render(request, 'dashboard.html')
    
class ErrorView(APIView):
    def get(self, request):
        return render(request, 'error.html')


class UserList(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return User.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class UserDetail(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, pk, *args, **kwargs):
        user = self.get_queryset(pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk, *args, **kwargs):
        user = self.get_queryset(pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk, *args, **kwargs):
        user = self.get_queryset(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)