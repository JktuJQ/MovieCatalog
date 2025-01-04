from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('<int:poll_id>/submit/', views.submit_poll, name='submit_poll'),
    path('<int:poll_id>/statistics/', views.poll_statistics, name='poll_statistics'),
]
