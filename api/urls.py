from atexit import register
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path



urlpatterns = [
    path('task-list/', views.TaskList.as_view(), name = 'task-list'),
    path('task-detail/<int:pk>', views.TaskDetail.as_view(), name = 'task-detail'),
    path('register/', views.Registraion, name='register'),
    # path('task-list/', views.task_list, name="task-list"),
    # path('task-detail/<int:pk>/', views.task_detail, name='task-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)