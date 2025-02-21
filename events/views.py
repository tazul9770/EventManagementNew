from django.shortcuts import render, redirect
from events.forms import EventModelForm, EventDetailForm
from events.models import Event, EventDetail
from django.db.models import Count, Q
from django.contrib import messages
from events.models import RSVP
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.http import Http404

def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@user_passes_test(is_organizer, login_url='no-permission')
def organizer_dashboard(request):
    type = request.GET.get('type', 'all')
    counts = Event.objects.aggregate(
        total = Count('id'),
        ongoing = Count('id', filter=Q(status='ONGOING')),
        completed = Count('id', filter=Q(status='COMPLETED')),
        upcoming = Count('id', filter=Q(status='UPCOMING'))
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
        "events":events,
        "counts":counts
    }
    return render(request, 'dashboard/organizer_dash.html', context)

@login_required
def user_dashboard(request):
    type = request.GET.get('type', 'all')
    counts = Event.objects.aggregate(
        total = Count('id'),
        ongoing = Count('id', filter=Q(status='ONGOING')),
        completed = Count('id', filter=Q(status='COMPLETED')),
        upcoming = Count('id', filter=Q(status='UPCOMING'))
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
        "events":events,
        "counts":counts
    }
    return render(request, 'dashboard/user_dash.html', context)

@login_required
#@permission_required('events.add_event', login_url='no-permission')
def create_event(request):
    form = EventModelForm()
    detail_form = EventDetailForm()
    if request.method == 'POST':
        form = EventModelForm(request.POST)
        detail_form = EventDetailForm(request.POST, request.FILES)
        if form.is_valid() and detail_form.is_valid():
            event = form.save()
            event_detail = detail_form.save(commit=False)
            event_detail.event = event
            event_detail.save()
            messages.success(request, "Event Created Successfully!")
            return redirect('create-event')
    return render(request, 'event_form.html', {"form":form, 'detail_form':detail_form})


@login_required
#@permission_required('events.change_event', login_url='no-permission')
def update_event(request, id):
    event = Event.objects.get(id=id)
    form = EventModelForm(instance=event)
    if event.details:
        detail_form = EventDetailForm(instance=event.details)
    if request.method == 'POST':
        form = EventModelForm(request.POST, instance=event)
        detail_form = EventDetailForm(request.POST, instance=event.details)
        if form.is_valid() and detail_form.is_valid():
            event = form.save()
            event_detail = detail_form.save(commit=False)
            event_detail.event = event
            event_detail.save()
            messages.success(request, "Event updated Successfully!")
            return redirect('update-event', id)
    return render(request, 'event_form.html', {"form":form, 'detail_form':detail_form})

@login_required
@permission_required('events.delete_event', login_url='no-permission')
def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Event deleted successfully")
        return redirect('organizer-dashboard')
    else:
        messages.success(request, "Something wrong!")
        return redirect('organizer-dashboard')

def event_detail(request, id):
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

