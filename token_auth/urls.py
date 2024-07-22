# urls.py
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, TodoItemListCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('todo-list/', TodoItemListCreateView.as_view(), name='todo-list'),
]
