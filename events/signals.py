from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event

#@receiver(m2m_changed, sender=Event.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [p.email for p in instance.assigned_to.all()]
        send_mail(
            "New Task Assigned",
            f"You have been assigned to the task: {instance.title}",
            "tazulislam42569835@gmail.com",
            assigned_emails,
            fail_silently=False,
        )

@receiver(post_delete, sender=Event)
def delete_associate_details(sender, instance, **kwargs):
    if hasattr(instance, 'details'): 
        instance.details.delete()
        print(f"Deleted details for event: {instance.title}")