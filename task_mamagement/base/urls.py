from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', admin_panel, name='admin-panel'),
    path('login/', login_view, name='login-page'),
    path('logout/', logout_view, name='logout'),
    path('add-user/', add_user, name='add-user'),
    path('edit-user/<int:pk>/', edit_user, name='edit-user'),
    path('add-task/', add_task, name='add-task'),
    path('edit-task/<int:pk>', edit_task, name='edit-task'),
    path('promote-user/<int:pk>', promote_user, name='promote-user'),
    path('demote-user/<int:pk>', demote_user, name='demote-user'),
    path('delete-user/<int:pk>', delete_user, name='delete-user'),
    path('delete-task/<int:pk>', delete_task, name='delete-task'),

    path('view-tasks/', TaskListView.as_view(), name='view-tasks'),
    path('update-tasks/<int:pk>/', TaskUpdateView.as_view(), name='update-tasks'),
    path('view-report/<int:pk>/', TaskReportView.as_view(), name='view-report'),
]