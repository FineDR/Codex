from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserTBManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class UserTB(AbstractUser):
    userID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100, blank=True, null=True)
    surName = models.CharField(max_length=100)
    passport = models.ImageField(upload_to='passport_photos/', blank=True, null=True)  # Modified field
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    role = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    confirmPassword = models.CharField(max_length=128)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserTBManager()

    def __str__(self):
        return f"{self.firstName} {self.surName}"
class StudentTB(models.Model):
    studentID = models.AutoField(primary_key=True)
    enrollmentDate = models.DateField()
    maritalStatus = models.CharField(max_length=10)
    nidaNumber = models.CharField(max_length=20, unique=True)
    program = models.CharField(max_length=100)
    regionName = models.CharField(max_length=255)
    userID = models.OneToOneField(UserTB, on_delete=models.CASCADE, related_name='student_profile')

    def __str__(self):
        return f"Student {self.userID.firstName} {self.userID.surName}"



class AppointmentsTB(models.Model):
    APPOINTMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]
    
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('counselor', 'Counselor'),
    ]
    
    appointment_id = models.AutoField(primary_key=True)
    userID = models.ForeignKey(UserTB, on_delete=models.CASCADE, related_name='appointments_made')
    receiverID = models.ForeignKey(UserTB, on_delete=models.CASCADE, related_name='appointments_received', default=1)
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    appointment_time = models.DateTimeField()

    def __str__(self):
        return f"Appointment {self.appointment_id} by {self.userID.firstName} for {self.receiverID.firstName} on {self.appointment_time}"

"""Resources Management...................................................."""
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # video_file = models.FileField(upload_to='videos/')
    video_file = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
"""this is Resource model....................................................................."""
class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('psychosocial', 'Psychosocial'),
    ]

    resourceID = models.AutoField(primary_key=True)
    uploadedBy = models.ForeignKey('UserTB', on_delete=models.CASCADE, related_name='created_resources')  # Ensure 'UserTB' is defined
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_path = models.FileField(upload_to='resources/')  # Removed 'media/' from upload_to
    tags = models.CharField(max_length=255, blank=True)  # Made tags optional
    upload_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title
"""Feedback Management...................................................."""
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserTB, on_delete=models.CASCADE)
    feedback_txt = models.TextField()
    rating = models.IntegerField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.feedback_id} by {self.user_id.email}"


"""this is the forumTB model start..................................................."""


class ForumTB(models.Model):
    CATEGORY_CHOICES = [
        ('academics', 'Academics'),
        ('psychosocials', 'Psychosocials'),
        ('groups', 'Groups'),
    ]

    forumID = models.AutoField(primary_key=True)
    createdBy = models.ForeignKey('UserTB', on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='academics')

    def __str__(self):
        return str(self.forumID)
    
"""this is the forumTB model end................................................................"""



"""This is participantTB start...................................................................."""

class ParticipantTB(models.Model):
    participant_id = models.AutoField(primary_key=True)
    userID = models.ForeignKey('UserTB', on_delete=models.CASCADE)
    forumID = models.ForeignKey('ForumTB', on_delete=models.CASCADE)
    joinedAt = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"User {self.userID.firstName} in Forum {self.forumID.title}"


"""This is participantTB end...................................................................."""


"""This is postTB start...................................................................."""

class PostTB(models.Model):
    POST_CATEGORY_CHOICES = [
        ('academics', 'Academics'),
        ('psychosocials', 'Psychosocials'),
        ('groups', 'Groups'),
    ]

    postID = models.AutoField(primary_key=True)
    content = models.TextField()
    createdBy = models.ForeignKey('UserTB', on_delete=models.CASCADE)
    forumID = models.ForeignKey('ForumTB', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=POST_CATEGORY_CHOICES, blank=True, null=True)
    createdAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post {self.postID} in Forum {self.forumID.title}"
"""This is postTB end...................................................................."""

"""This is notificationTB start...................................................................."""

class NotificationTB(models.Model):
    notification_id = models.AutoField(primary_key=True)
    userID = models.ForeignKey('UserTB', on_delete=models.CASCADE)
    forumID = models.ForeignKey('ForumTB', on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification {self.notification_id} for User {self.userID.firstName}"

"""This is notificationTB end...................................................................."""
    
# class Feedback(models.Model):
#     STUDENT = 'student'
#     COUNSELLOR = 'counsellor'
#     TUTOR = 'tutor'
    
#     FEEDBACK_TYPE_CHOICES = [
#         (STUDENT, 'Student'),
#         (COUNSELLOR, 'Counsellor'),
#         (TUTOR, 'Tutor'),
#     ]

#     feedback_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(UserTB, on_delete=models.CASCADE)
#     feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
#     rating = models.IntegerField()
#     comments = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Feedback {self.feedback_id} by {self.user.username}'


"""Logs Management...................................................."""
# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('tutor', 'Tutor'),
#         ('counsellor', 'Counsellor'),
#         ('student', 'Student'),
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class UserActivityLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('view', 'View'),
        ('delete', 'Delete'),
    ]
    userID = models.ForeignKey(UserTB, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    details = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.userID.email} - {self.action} - {self.createdAt}"
    
class Notification_USER(models.Model):
    NOTIFICATION_TYPES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )

    userID = models.ForeignKey(UserTB, on_delete=models.CASCADE)
    message_content = models.TextField()
    receiverID = models.ForeignKey(UserTB, related_name='received_notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.userID} to {self.receiverID}"