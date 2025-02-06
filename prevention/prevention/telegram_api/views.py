
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserRequest
from .serializers import UserRequestSerializer

# Отримання всіх запитів
@api_view(['GET'])
def get_user_requests(request):
    try:
        user_requests = UserRequest.objects.all()
        serializer = UserRequestSerializer(user_requests, many=True)
        return Response(serializer.data)
    except UserRequest.DoesNotExist:
        return Response({"detail": "No user requests found."}, status=status.HTTP_404_NOT_FOUND)

# Створення нового запиту
@api_view(['POST'])
def create_user_request(request):
    try:
        serializer = UserRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
