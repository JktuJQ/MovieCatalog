from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('<int:poll_id>/submit/', views.submit_poll, name='submit_poll'),
    path('<int:poll_id>/statistics/', views.poll_statistics, name='poll_statistics'),
    path('create/<int:film_id>/', views.create_poll, name='create_poll'),
    path('confirm-delete/<int:poll_id>/', views.confirm_delete_poll, name='confirm_delete_poll'),
    path('delete/<int:poll_id>/', views.delete_poll, name='delete_poll'),
]
