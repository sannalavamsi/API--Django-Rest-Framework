from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')



urlpatterns =[
    #path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls')),
    path('api/', views.apiOverview,name="api-overview"),
    path('task-list/', views.taskList,name="task-list"),
    path('task-detail/<str:pk>/', views.taskDetail,name="task-detail"),
    path('task-create/', views.taskCreate,name="task-create"),
    path('task-update/<str:pk>/', views.taskUpdate,name="task-update"),
    path('task-delete/<str:pk>/', views.taskDelete,name="task-delete"),
    #class based APIView
    path('classtask/',views.TaskViewList.as_view()),
    path('classtaskdetail/<str:pk>/',views.TaskViewDetail.as_view()),
]

urlpatterns += router.urls