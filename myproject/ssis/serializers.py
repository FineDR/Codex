from rest_framework import serializers
from .models import Feedback, ForumTB, NotificationTB,Notification_USER, ParticipantTB, PostTB, UserActivityLog, UserTB, StudentTB,AppointmentsTB,Video,Resource

class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentsTB
        fields = '__all__'
        extra_kwargs = {
            'status': {
                'error_messages': {
                    'invalid_choice': 'Please select a valid status: pending, confirmed, or canceled.'
                }
            },
            'user_type': {
                'error_messages': {
                    'invalid_choice': 'Please select a valid user type: Student, Tutor, or Counselor.'
                }
            }
        }
class UserTBSerializer(serializers.ModelSerializer):
    passport = serializers.ImageField(required=False)  # Modify passport to ImageField

    class Meta:
        model = UserTB
        fields = ['userID', 'firstName', 'middleName', 'surName', 'passport', 'email', 'phoneNumber', 'gender', 'role', 'password', 'confirmPassword']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirmPassword': {'write_only': True}
        }

    def create(self, validated_data):
        passport = validated_data.pop('passport', None)  # Pop passport from validated_data
        user = UserTB.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            firstName=validated_data['firstName'],
            middleName=validated_data.get('middleName', ''),
            surName=validated_data['surName'],
            phoneNumber=validated_data['phoneNumber'],
            gender=validated_data['gender'],
            role=validated_data['role']
        )
        
        if passport:  # Save passport image if provided
            user.passport = passport
            user.save()

        return user

class StudentTBSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTB
        fields = ['userID', 'enrollmentDate', 'maritalStatus', 'nidaNumber', 'program', 'regionName']
        # Ensure 'userID' is included in the fields

class ForumTBSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=ForumTB.CATEGORY_CHOICES)  # Handles choices field
    createdAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ForumTB
        fields = ['forumID', 'createdBy', 'content', 'category', 'createdAt']
        read_only_fields = ['forumID', 'createdBy', 'createdAt']
        
"""this is PostSerializer......................................................."""

class PostTBSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTB
        fields = ['postID', 'content', 'createdBy', 'forumID', 'category', 'createdAt']
        read_only_fields = ['postID', 'createdAt', 'createdBy']

"""This is participantSerializer..................................................."""

class ParticipantTBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantTB
        fields = ['participant_id', 'userID', 'forumID', 'joinedAt']
        
"""this is notification serializer.............................................."""
class NotificationTBSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTB
        fields = '__all__'


"""Video Resource Serializers...................................................."""
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'uploaded_at']


"""Feedback Serializers...................................................."""
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['feedback_id', 'user_id', 'feedback_txt', 'rating', 'date_submitted']

# class FeedbackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feedback
#         fields = '__all__'

#     def validate_user(self, value):
#         if not UserTB.objects.filter(id=value.id).exists():
#             raise serializers.ValidationError("User not found in the database.")
#         if value.profile.role not in ['student', 'counsellor', 'tutor']:
#             raise serializers.ValidationError("Only students, counsellors, and tutors can submit feedback.")
#         return value


"""Logs Serializers...................................................."""

class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = '__all__'

"""this is Resource serilizer................................................"""


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['resourceID', 'uploadedBy', 'title', 'description', 'file_path', 'tags', 'upload_date', 'category']



"""this is for notification"""

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification_USER
        fields = '__all__'











