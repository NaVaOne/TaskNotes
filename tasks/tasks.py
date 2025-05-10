from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from tasks.models import Task

@shared_task
def send_deadline_notification(task_id):
    try:
        task = Task.objects.get(id=task_id)

        if not task.is_alerted and not task.is_completed:
            subject = f'Уведомление о дедлайне для задачи "{task.title}"'
            message = f'Дедлайн для задачи "{task.title}" на {task.deadline.strftime("%Y-%m-%d %H:%M")} уже наступил.'
            send_mail(
                subject,
                message, 
                settings.EMAIL_HOST_USER, 
                [task.user.email],
                fail_silently=False,
                )
            task.is_alerted = True
            task.save()

    except Task.DoesNotExist:
        pass

@shared_task
def schedule_notification(task_id):
    """
    Планирует выполнение send_deadline_notification за 5 минут до дедлайна.
    """
    try:
        task = Task.objects.get(id=task_id)
        
        # Отменяем предыдущее уведомление (если было)
        if task.celery_task_id:
            from todo_project.celery import app  
            app.control.revoke(task.celery_task_id, terminate=True)
        
        # Вычисляем время отправки (за 5 минут до дедлайна)
        eta = task.deadline - timezone.timedelta(minutes=5)
        
        # Проверяем, что время еще не прошло
        if eta > timezone.now():
            result = send_deadline_notification.apply_async(args=[task.id], eta=eta)
            task.celery_task_id = result.id
            task.save()
            
    except Task.DoesNotExist:
        pass