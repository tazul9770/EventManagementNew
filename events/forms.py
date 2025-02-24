from django import forms
from .models import Event, EventDetail
from django.contrib.auth import get_user_model

User = get_user_model()


class EventModelForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'due_date', 'time', 'status', 'assigned_to']
        widgets = {
            'due_date': forms.SelectDateWidget,
        }

class EventDetailForm(forms.ModelForm):
    class Meta:
        model = EventDetail
        fields = ['category', 'notes', 'asset']

