from django.urls import path
from . import views

urlpatterns = [
    path("", views.EventList.as_view(), name="home"),
    path("add_event/", views.add_event, name="add_event"),
    path("delete_event/<int:event_id>/", views.delete_event, name="delete_event"),
    path("edit_event/<int:edit_id>/", views.edit_event, name="edit_event"),
    path("view_event/<int:event_id>/", views.view_event, name="view_event"),
    path("edit_participant/<int:event_id>/", views.edit_participant, name="edit_participant"),
    path("random_santa/<int:event_id>/", views.random_santa, name="random_santa"),
    path("invite_participant/<int:participant_id>/", views.invite_participant, name="invite_participant"),    
]
