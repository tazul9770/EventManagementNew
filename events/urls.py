
from django.urls import path
from events.views import dashboard,CreateEvent,OrganizerDashboard, UserDashboard, UpdateEvent, DeleteEvent, EventDetail

urlpatterns = [
    path('create_event/', CreateEvent.as_view(), name='create-event'),
    path("update_event/<int:id>", UpdateEvent.as_view(), name="update-event"),
    path("delete_event/<int:id>", DeleteEvent.as_view(), name="delete-event"),
    path('event_detail/<int:id>/', EventDetail.as_view(), name='event-detail'),
    path('dashboard/', dashboard, name='dashboard'),
    path('organizer_dashboard/', OrganizerDashboard.as_view(), name='organizer-dashboard'),
    path('user_dashboard/', UserDashboard.as_view(), name='user-dashboard'),

]