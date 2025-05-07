from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
User = get_user_model()

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_alerted = models.BooleanField(default=False, verbose_name='уведомдения отправлено')
    celery_task_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID задачи Celery")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title
    
    def clean(self):
        super().clean()
        if self.deadline and self.deadline<= timezone.now():
            raise ValidationError({'deadline': 'Дедлайн не может быть в прошлом.'})
