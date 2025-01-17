from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.poll_list, name='polls'),
    path('<int:poll_id>/submit/', views.submit_poll, name='submit_poll'),
    path('<int:poll_id>/statistics/', views.poll_statistics, name='poll_statistics'),
    path('create/poll/<int:film_id>/', views.create_poll, name='create_poll'),
    path('create/question/<int:poll_id>/', views.create_question, name='create_question'),
    path('create/choice/<int:question_id>/', views.create_choice, name='create_choice'),
    path('confirm_delete_poll/<int:poll_id>/', views.confirm_delete_poll, name='confirm_delete_poll'),
    path('confirm_delete/question/<int:question_id>', views.delete_question, name='confirm_delete_question'),
    path('update/poll/<int:poll_id>/', views.update_poll, name='update_poll'),
    path('update/question/<int:question_id>', views.update_question, name='update_question'),
    path('delete/<int:poll_id>/', views.delete_poll, name='delete_poll'),
]
