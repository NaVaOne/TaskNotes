# tasks/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from .tasks import schedule_notification

# @receiver(post_save, sender=Task)
# def task_created_handler(sender, instance, created, **kwargs):
#     if created:
#         # Планируем уведомление при создании задачи
#         schedule_notification.delay(instance.id)