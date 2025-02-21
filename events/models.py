from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    STATUS_CHOICES = [
        ('UPCOMING', 'upcoming'),
        ('ONGOING', 'ongoing'),
        ('COMPLETED', 'completed')
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPCOMING')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ManyToManyField(User, related_name='events', blank=True)

    def __str__(self):
        return self.title
    
class EventDetail(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='details')
    category = models.CharField(max_length=50, choices=[('CONF', 'Conference'), ('MEETUP', 'Meetup'), ('WORKSHOP', 'Workshop')], default='MEETUP')
    asset = models.ImageField(upload_to='events_asset',  blank=True, null=True,
                              default="events_asset/default_img.jpg")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details for {self.event.title}"

class RSVP(models.Model):
    user = models.ManyToManyField(User, related_name="rsvps")
    event = models.ManyToManyField(Event, related_name="rsvps")
