
from django.db import models

class UserRequest(models.Model):
    user_id = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Запит від користувача {self.user_id}"
