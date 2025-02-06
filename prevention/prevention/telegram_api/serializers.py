from rest_framework import serializers
from prevention.prevention.telegram_api.models import UserRequest

class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = ['id', 'user_id', 'message', 'timestamp']