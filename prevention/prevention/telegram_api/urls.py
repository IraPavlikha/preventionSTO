from django.urls import path
from .views import UserRequestSerializer

urlpatterns = [
    path('user_requests/', UserRequestSerializer.get_user_requests, name='get_user_requests'),  # для отримання запитів
    path('user_requests/create/', UserRequestSerializer.create_user_request, name='create_user_request'),  # для створення нового запиту
]