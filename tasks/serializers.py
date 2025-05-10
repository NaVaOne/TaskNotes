from rest_framework import serializers
from .models import Task
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Task
        fields = ('id','user' ,'title', 'description', 'deadline', 'is_completed')
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_alerted', 'celery_task_id')

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Дедлайн не может быть в прошлом.")
        return value

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'is_completed','deadline')  