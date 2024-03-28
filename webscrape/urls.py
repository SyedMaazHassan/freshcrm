from django.urls import path, include

from . import views

urlpatterns = [
    path('hktdc-tasks', views.hktdc_tasks, name='hktdc_tasks'),    
    path('hktdc-tasks/<id>/results', views.hktdc_tasks_result, name='hktdc_tasks_result')
]
