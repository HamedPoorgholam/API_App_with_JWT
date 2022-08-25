from atexit import register
from . import views
from .views import TaskViewset
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView



router = DefaultRouter()
router.register('task', TaskViewset, basename='task')

urlpatterns = [
    path('viewset', include(router.urls)),
    path('task-list/', views.TaskList.as_view(), name = 'task-list'),
    path('task-detail/<int:pk>', views.TaskDetail.as_view(), name = 'task-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.Registraion, name='register'),
    # path('task-list/', views.task_list, name="task-list"),
    # path('task-detail/<int:pk>/', views.task_detail, name='task-detail'),
]


    