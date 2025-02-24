from django.shortcuts import render, redirect
from events.forms import EventModelForm, EventDetailForm
from events.models import Event, EventDetail
from django.db.models import Count, Q
from django.contrib import messages
from events.models import RSVP
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.http import Http404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@method_decorator(user_passes_test(is_organizer, login_url='no-permission'), name='dispatch')
class OrganizerDashboard(View):
    def get(self, request):
        type = request.GET.get('type', 'all')
        counts = Event.objects.aggregate(
            total=Count('id'),
            ongoing=Count('id', filter=Q(status='ONGOING')),
            completed=Count('id', filter=Q(status='COMPLETED')),
            upcoming=Count('id', filter=Q(status='UPCOMING'))
        )

        base_query = Event.objects.prefetch_related('assigned_to')
        
        if type == 'upcoming':
            events = base_query.filter(status='UPCOMING')
        elif type == 'ongoing':
            events = base_query.filter(status='ONGOING')
        elif type == 'completed':
            events = base_query.filter(status='COMPLETED')
        elif type == 'all':
            events = base_query.all()
        else:
            events = base_query.none()

        context = {
            "events": events,
            "counts": counts
        }
        return render(request, 'dashboard/organizer_dash.html', context)
    

@method_decorator(login_required(login_url='login'), name='dispatch') 
class UserDashboard(View):
    def get(self, request):
        type = request.GET.get('type', 'all')
        counts = Event.objects.aggregate(
            total=Count('id'),
            ongoing=Count('id', filter=Q(status='ONGOING')),
            completed=Count('id', filter=Q(status='COMPLETED')),
            upcoming=Count('id', filter=Q(status='UPCOMING'))
        )

        base_query = Event.objects.prefetch_related('assigned_to')
        
        if type == 'upcoming':
            events = base_query.filter(status='UPCOMING')
        elif type == 'ongoing':
            events = base_query.filter(status='ONGOING')
        elif type == 'completed':
            events = base_query.filter(status='COMPLETED')
        elif type == 'all':
            events = base_query.all()
        else:
            events = base_query.none()

        context = {
            "events": events,
            "counts": counts
        }
        return render(request, 'dashboard/user_dash.html', context)

@method_decorator(login_required, name='dispatch')   
class CreateEvent(View):
    def get(self,  request):
        form = EventModelForm()
        detail_form = EventDetailForm()
        return render(request, 'event_form.html', {"form":form, "detail_form": detail_form})
    def post(self, request):
        form = EventModelForm(request.POST)
        detail_form = EventDetailForm(request.POST, request.FILES)
        if form.is_valid and detail_form.is_valid():
            event = form.save()
            event_detail = detail_form.save(commit=False)
            event_detail.event = event
            event_detail.save()
            messages.success(request, "Event created successfully!")
            return redirect('create-event')
        return render(request, 'event_form.html', {"form":form, "detail_form": detail_form})

@method_decorator(login_required, name='dispatch')   
class UpdateEvent(View):
    def get(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            messages.error(request, "Event not found!")

        form = EventModelForm(instance=event)
        event_details_instance = event.details if hasattr(event, 'details') else None
        detail_form = EventDetailForm(instance=event_details_instance)
        
        return render(request, 'event_form.html', {"form": form, "detail_form": detail_form})

    def post(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            messages.error(request, "Event not found!")
            return redirect('some-view-name')

        form = EventModelForm(request.POST, instance=event)
        event_details_instance = event.details if hasattr(event, 'details') else None
        detail_form = EventDetailForm(request.POST, instance=event_details_instance)

        if form.is_valid() and detail_form.is_valid():
            event = form.save()
            event_detail = detail_form.save(commit=False)
            event_detail.event = event
            event_detail.save()
            
            messages.success(request, "Event updated successfully!")
            return redirect('update-event', id=id)
        
        return render(request, 'event_form.html', {"form": form, "detail_form": detail_form})

class DeleteEvent(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'events.delete_event'
    login_url = 'no-permission'
    def post(self, request, id):
        try:
            event = Event.objects.get(id=id)
            event.delete()
            messages.success(request, "Event deleted successfully!")
        except Event.DoesNotExist:
            messages.error(request, "Event Not found")
        return redirect('organizer-dashboard')
    
class EventDetail(View):
    def get(self, request, id):
        try:
            event = Event.objects.select_related("details").prefetch_related("assigned_to", "rsvps__user").get(id=id)
        except Event.DoesNotExist:
            raise Http404("Event not found")

        rsvp_users = RSVP.objects.filter(event=event).prefetch_related("user")

        context = {
            "event": event,
            "rsvp_users": rsvp_users,
        }
        return render(request, 'event_detail.html', context)