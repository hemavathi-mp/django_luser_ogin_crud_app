from django.urls import path
from .views import UserList,UserDetail,LoginView,DashboardView,ErrorView

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('login_view/', LoginView.as_view(), name='login-view'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('error/', ErrorView.as_view(), name='error'),


]