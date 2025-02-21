
from django.urls import path
from events.views import create_event, dashboard, organizer_dashboard, user_dashboard, update_event, delete_event, event_detail

urlpatterns = [
    path('create_event/', create_event, name='create-event'),
    path("update_event/<int:id>", update_event, name="update-event"),
    path("delete_event/<int:id>", delete_event, name="delete-event"),
    path('event_detail/<int:id>/', event_detail, name='event-detail'),
    path('dashboard/', dashboard, name='dashboard'),
    path('organizer_dashboard/', organizer_dashboard, name='organizer-dashboard'),
    path('user_dashboard/', user_dashboard, name='user-dashboard'),

]