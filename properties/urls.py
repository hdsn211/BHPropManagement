from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.public_home, name='public_home'),
    path('property/<int:property_id>/rooms/', views.public_room_list, name='public_room_list'),
    
    # Admin Room CRUD
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:id>/', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:id>/', views.delete_room, name='delete_room'),
    path('rooms/<int:id>/', views.room_detail, name='room_detail'),
]