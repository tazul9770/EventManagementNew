from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user, admin_dashboard, assign_role, create_group, group_list, rsvp_event, cancel_rsvp

urlpatterns = [
    path('sign_up/', sign_up, name='sign-up'),
    path('sign_in/', sign_in, name='sign-in'),
    path('logout/', sign_out, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin_dashboard/', admin_dashboard, name='admin-dashboard'),
    path('assign_role/<int:user_id>/', assign_role, name='assign-role'),
    path('create_group/', create_group, name='create-group'),
    path('group-list/', group_list, name='group-list'),
    path('rsvp/<int:id>/', rsvp_event, name='rsvp-event'),
    path('cancel_rsvp/<int:id>/', cancel_rsvp, name='cancel-rsvp')
]
