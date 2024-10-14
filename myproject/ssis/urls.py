from django.contrib import admin
from django.urls import path
from .views import (
    AppointmentView,
    FeedbackView,
    ForumView,
    ParticipantView,
    PostView,
    UserActivityLogView,
    UserLoginView,
    UserLogoutView,
    home,
    RegisterView,
    ResourceView,
    NotificationView,
    NotificationUSER,
    StudentDetailView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Root URL for your app
    path('', home, name='home'),

    # User registration, login, logout
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', RegisterView.as_view(), name='user-list'),
    path('student/<int:user_id>/', StudentDetailView.as_view(), name='student-detail'),
    path('users/<str:user_id>/', RegisterView.as_view(), name='user-detail'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Appointments
    path('appointments/', AppointmentView.as_view(), name='appointment-list'),  # create=POST, retrieve all=GET
    path('appointments/<int:appointment_id>/', AppointmentView.as_view(), name='appointment-detail'),  # update=PUT, delete=DELETE, retrieve specific=GET

    # Forum
    path('forums/', ForumView.as_view(), name='forum-list'),  # create=POST, retrieve all=GET
    path('forums/<int:forum_id>/', ForumView.as_view(), name='forum-detail'),

    path('forums/<int:forum_id>/posts/', PostView.as_view(), name='post-list'),  # create=POST, retrieve all posts=GET
    path('forums/<int:forum_id>/posts/<int:post_id>/', PostView.as_view(), name='post-detail'),  # update=PUT, retrieve specific details=GET, delete=DELETE

    path('forums/<int:forum_id>/participants/', ParticipantView.as_view(), name='participant-list'),  # All actions

    path('forums/<int:forum_id>/notifications/', NotificationView.as_view(), name='notification-list'),  # create=POST, retrieve all=GET
    path('forums/<int:forum_id>/notifications/<int:notification_id>/', NotificationView.as_view(), name='notification-detail'),  # update=PUT, delete=DELETE

    # Resources
    path('resources/', ResourceView.as_view(), name='resource-list'),
    path('resources/<int:resource_id>/', ResourceView.as_view(), name='resource-detail'),

    # Feedback
    path('feedback/', FeedbackView.as_view(), name='submit-feedback'),
    # Uncomment these if you have FeedbackListView and FeedbackDeleteView defined
    # path('feedback/list/', FeedbackListView.as_view(), name='feedback-list'),
    # path('feedback/delete/<int:pk>/', FeedbackDeleteView.as_view(), name='delete-feedback'),

    # User activity logs
    path('activity-log/', UserActivityLogView.as_view(), name='activity-log-list'),  # For GET (view logs)
    path('activity-log/create/', UserActivityLogView.as_view(), name='activity-log-create'),  # For POST (create log)

    path('notifications/', NotificationUSER.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/', NotificationUSER.as_view(), name='notification-detail'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
