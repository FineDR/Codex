from contextvars import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feedback, UserTB, StudentTB,AppointmentsTB,Resource,Notification_USER
# from .serializers import FeedbackSerializer, ForumTBSerializer, ParticipantTBSerializer, PostTBSerializer, UserActivityLogSerializer, UserTBSerializer, StudentTBSerializer,AppointmentsSerializer,VideoSerializer

from .models import Feedback, UserTB, StudentTB,AppointmentsTB,Video,NotificationTB, ForumTB, ParticipantTB, PostTB, UserActivityLog
from .serializers import FeedbackSerializer,NotificationSerializer, UserTBSerializer,ParticipantTBSerializer, StudentTBSerializer,PostTBSerializer,AppointmentsSerializer,ResourceSerializer,NotificationTBSerializer,ForumTBSerializer,UserActivityLogSerializer

from datetime import date
from rest_framework.views import status
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""This is about home page...................................................."""
def home(request):
    return HttpResponse("Welcome to the Student Support Information System (SSIS)!")

class RegisterView(APIView):

    # Override permission_classes based on the request method
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]  # Allow anyone to access the registration endpoint
        return [IsAuthenticated()]  # All other requests require authentication

    def post(self, request):
        """
        Register a new user. If the user is a student, additional student information is also saved.
        """
        serializer = UserTBSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user.role.lower() == 'student':
            student_data = {
                'userID': user.userID,  # Ensure this matches the field name in StudentTB
                'enrollmentDate': request.data.get('enrollmentDate', date.today()),
                'maritalStatus': request.data.get('maritalStatus', 'Single'),
                'nidaNumber': request.data.get('nidaNumber', 'N/A'),
                'program': request.data.get('program', 'General'),
                'regionName': request.data.get('regionName', 'Unknown'),
            }

            student_serializer = StudentTBSerializer(data=student_data)
            student_serializer.is_valid(raise_exception=True)
            student_serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, user_id):
        """
        Update an existing user.
        """
        user = get_object_or_404(UserTB, userID=user_id)
        serializer = UserTBSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        if updated_user.role.lower() == 'student':
            student_data = {
                'userID': updated_user.userID,
                'enrollmentDate': request.data.get('enrollmentDate'),
                'maritalStatus': request.data.get('maritalStatus'),
                'nidaNumber': request.data.get('nidaNumber'),
                'program': request.data.get('program'),
                'regionName': request.data.get('regionName'),
            }

            student, created = StudentTB.objects.update_or_create(
                userID=updated_user,
                defaults=student_data
            )

            student_serializer = StudentTBSerializer(student)
            return Response({
                'user': serializer.data,
                'student': student_serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        """
        Delete an existing user.
        """
        user = get_object_or_404(UserTB, userID=user_id)
        user.delete()

        # Also delete related student data if user is a student
        if user.role.lower() == 'student':
            StudentTB.objects.filter(userID=user).delete()

        return Response({
            'message': 'User and related data deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, user_id=None):
        """
        Retrieve a specific user or list all users.
        """
        if user_id:
            user = get_object_or_404(UserTB, userID=user_id)
            serializer = UserTBSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            users = UserTB.objects.all()
            serializer = UserTBSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class StudentDetailView(APIView):
    """
    Retrieve a specific student or list all students.
    """
    permission_classes=[IsAuthenticated]
    def get(self, request, user_id=None):
        if user_id:
            # Retrieve a specific student's details
            student = get_object_or_404(StudentTB, userID=user_id)
            serializer = StudentTBSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Retrieve details of all students
            students = StudentTB.objects.all()
            serializer = StudentTBSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

"""This is login logic..........................................................."""



class UserLoginView(APIView):
    # permission_classes=[IsAuthenticated]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = None
        if '@' in email:
            try:
                user = UserTB.objects.get(email=email)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            role = user.role
            first_name = user.firstName
            middle_name = user.middleName
            user_id = user.userID  # Retrieve userID
            # Log the user role
            logger.info(f'User role: {role}, First name: {first_name}, Middle name: {middle_name}')
            return Response({
                'token': token.key,
                'role': role,
                'first_name': first_name,
                'middle_name': middle_name,  # Include first name and middle name in the response
                'userID': user_id  # Include userID in the response
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
"""This is login logic..........................................................."""
    
"""This is logout logic......................................................"""

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Create a new appointment
        user_id = request.data.get('userID')
        try:
            user = UserTB.objects.get(userID=user_id)
        except UserTB.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentsSerializer(data=request.data)
        if serializer.is_valid():
            # Save the appointment with the user reference
            serializer.save(userID=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Log detailed validation errors for debugging
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, appointment_id=None):
        # Retrieve a specific appointment or list all appointments for a specific receiverID
        receiver_id = request.query_params.get('receiverID')

        if appointment_id:
            # Retrieve a specific appointment by ID
            appointment = get_object_or_404(AppointmentsTB, appointment_id=appointment_id)
            serializer = AppointmentsSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif receiver_id:
            # Filter appointments by receiverID
            appointments = AppointmentsTB.objects.filter(receiverID=receiver_id)
            serializer = AppointmentsSerializer(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Return all appointments if no specific filters are applied
            appointments = AppointmentsTB.objects.all()
            serializer = AppointmentsSerializer(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, appointment_id):
        # Update a specific appointment
        appointment = get_object_or_404(AppointmentsTB, appointment_id=appointment_id)

        # Handle appointment confirmation or cancellation
        if 'confirm' in request.data:
            if request.data['confirm'] == 'true':
                appointment.status = 'confirmed'
            elif request.data['confirm'] == 'false':
                appointment.status = 'canceled'
            else:
                return Response({"error": "Invalid confirm value."}, status=status.HTTP_400_BAD_REQUEST)
            appointment.save()
            return Response({
                'message': f'Appointment {appointment.status} successfully',
                'appointmentID': appointment.appointment_id
            }, status=status.HTTP_200_OK)

        # Handle other updates
        serializer = AppointmentsSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Appointment updated successfully',
                'appointmentID': appointment.appointment_id
            }, status=status.HTTP_200_OK)

        # Log detailed validation errors for debugging
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, appointment_id):
        # Delete a specific appointment
        appointment = get_object_or_404(AppointmentsTB, appointment_id=appointment_id)
        appointment.delete()
        return Response({
            'message': 'Appointment deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
"""This is forum view start......................................................................"""

class ForumView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        content = request.data.get('content')
        user_id = request.data.get('createdBy')
        category = request.data.get('category')

        # Validate content and user_id
        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user_id:
            return Response({'error': 'createdBy is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the UserTB instance
        user = get_object_or_404(UserTB, pk=user_id)

        # Create a forum entry
        forum_entry = ForumTB.objects.create(
            createdBy=user,
            content=content,
            category=category
        )

        # Serialize and return the newly created forum entry
        serializer = ForumTBSerializer(forum_entry)
        return Response({
            'forumID': forum_entry.forumID,
            'message': 'Forum entry created successfully!',
            'forumEntry': serializer.data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, forum_id):
        forum_entry = get_object_or_404(ForumTB, pk=forum_id)

        # Update the content of the forum entry
        forum_entry.content = request.data.get('content', forum_entry.content)
        forum_entry.save()
        return Response({
            'forumID': forum_entry.forumID,
            'message': 'Forum entry updated successfully'
        }, status=status.HTTP_200_OK)

    def get(self, request, forum_id=None):
        if forum_id:
            forum_entry = get_object_or_404(ForumTB, pk=forum_id)
            serializer = ForumTBSerializer(forum_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            forums = ForumTB.objects.all()
            serializer = ForumTBSerializer(forums, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, forum_id):
        forum_entry = get_object_or_404(ForumTB, pk=forum_id)
        forum_entry.delete()
        return Response({'message': 'Forum entry deleted successfully'}, status=status.HTTP_200_OK)
    
"""This is forum view end......................................................................"""

class PostView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, forum_id):
        # Bind the post to the specific forum using forum_id
        forum = get_object_or_404(ForumTB, pk=forum_id)
        content = request.data.get('content')
        user_id = request.data.get('userID')
        category = request.data.get('category')

        # Retrieve the user by userID
        user = get_object_or_404(UserTB, pk=user_id)

        # Create the post
        post = PostTB.objects.create(
            content=content,
            createdBy=user,  # Use the user fetched by userID
            forumID=forum,
            category=category  # Use the category from the request
        )

        serializer = PostTBSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, forum_id, post_id=None):
        if post_id:
            # Retrieve a specific post
            post = get_object_or_404(PostTB, pk=post_id, forumID=forum_id)
            serializer = PostTBSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Retrieve all posts within the specific forum
            forum = get_object_or_404(ForumTB, pk=forum_id)
            posts = PostTB.objects.filter(forumID=forum)
            serializer = PostTBSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, forum_id, post_id):
        # Update a specific post
        post = get_object_or_404(PostTB, pk=post_id, forumID=forum_id)
        content = request.data.get('content')
        category = request.data.get('category')

        if content:
            post.content = content
        if category:
            post.category = category
        post.save()
        serializer = PostTBSerializer(post)
        return Response({
            'message': 'The post is updated successfully',
            'postID': post.postID
        }, status=status.HTTP_200_OK)

    def delete(self, request, forum_id, post_id):
        # Delete a specific post
        post = get_object_or_404(PostTB, pk=post_id, forumID=forum_id)
        post.delete()
        return Response({
            'message': 'The post is deleted successfully'
        }, status=status.HTTP_200_OK)
    
"""This is forum participant................................................."""

class ParticipantView(APIView):
    permission_classes=[IsAuthenticated]

    permission_classes = [IsAuthenticated]

    def post(self, request, forum_id):
        # Bind the participant to the specific forum using forum_id
        forum = get_object_or_404(ForumTB, pk=forum_id)

        # Check if the user is already a participant
        if ParticipantTB.objects.filter(userID=request.user, forumID=forum).exists():
            return Response({'message': 'You are already a participant in this forum.'}, status=status.HTTP_200_OK)

        # Create a new participant entry
        participant = ParticipantTB.objects.create(
            userID=request.user,
            forumID=forum
        )

        serializer = ParticipantTBSerializer(participant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, forum_id):
        # Retrieve all participants within the specific forum
        forum = get_object_or_404(ForumTB, pk=forum_id)
        participants = ParticipantTB.objects.filter(forumID=forum)

        serializer = ParticipantTBSerializer(participants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, forum_id):
        # Update the participant entry (assuming this is required, though it might not be typical)
        forum = get_object_or_404(ForumTB, pk=forum_id)
        participant = get_object_or_404(ParticipantTB, userID=request.user, forumID=forum)

        serializer = ParticipantTBSerializer(participant)
        return Response({
            'message': 'Participant updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, forum_id):
        # Remove the participant from the forum
        forum = get_object_or_404(ForumTB, pk=forum_id)
        participant = get_object_or_404(ParticipantTB, userID=request.user, forumID=forum)
        participant.delete()

        return Response({
            'message': 'Participant removed successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
"""this is notification view..................................................."""

class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, forum_id):
        # Bind the notification to the specific forum using forum_id
        forum = get_object_or_404(ForumTB, pk=forum_id)
        message = request.data.get('message')

        # Check if a similar notification already exists
        existing_notification = NotificationTB.objects.filter(
            userID=request.user,
            forumID=forum,
            message=message,
            read=False
        ).exists()

        if existing_notification:
            return Response({'message': 'Similar notification already exists.'}, status=status.HTTP_200_OK)

        # If no similar notification exists, create a new one
        notification = NotificationTB.objects.create(
            userID=request.user,
            forumID=forum,
            message=message,
            read=False
        )

        serializer = NotificationTBSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, forum_id):
        # Retrieve all notifications within the specific forum for the authenticated user
        forum = get_object_or_404(ForumTB, pk=forum_id)
        notifications = NotificationTB.objects.filter(forumID=forum, userID=request.user)

        serializer = NotificationTBSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, forum_id, notification_id):
        # Update a specific notification
        forum = get_object_or_404(ForumTB, pk=forum_id)
        notification = get_object_or_404(NotificationTB, pk=notification_id, userID=request.user, forumID=forum)

        # Optionally update fields, e.g., mark as read
        read = request.data.get('read', notification.read)
        message = request.data.get('message', notification.message)
        
        notification.read = read
        notification.message = message
        notification.save()

        serializer = NotificationTBSerializer(notification)
        return Response({
            'message': 'Notification updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, forum_id, notification_id):
        # Delete a specific notification
        forum = get_object_or_404(ForumTB, pk=forum_id)
        notification = get_object_or_404(NotificationTB, pk=notification_id, userID=request.user, forumID=forum)
        notification.delete()

        return Response({
            'message': 'Notification deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)



class ResourceView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        """Create a new resource"""
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, resource_id=None):
        """Retrieve a single resource or a list of resources"""
        if resource_id:
            resource = get_object_or_404(Resource, resourceID=resource_id)
            serializer = ResourceSerializer(resource)
            # Log the details of the retrieved resource
            logger.info(f'Retrieved resource with ID {resource_id}: {serializer.data}')
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            resources = Resource.objects.all().order_by('-upload_date')
            serializer = ResourceSerializer(resources, many=True)
            # Log the details of the retrieved resources
            logger.info(f'Retrieved resources: {serializer.data}')
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, resource_id):
        """Update an existing resource"""
        resource = get_object_or_404(Resource, resourceID=resource_id)
        serializer = ResourceSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, resource_id):
        """Delete an existing resource"""
        resource = get_object_or_404(Resource, resourceID=resource_id)
        resource.delete()
        return Response({"message": "Resource deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

    """Feedback Handling...................................................."""
    
class FeedbackView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                user = UserTB.objects.get(userID=user_id)
            except UserTB.DoesNotExist:
                return Response({"error": "User ID not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            feedbacks = Feedback.objects.filter(user_id=user_id)
        else:
            feedbacks = Feedback.objects.all()
        
        feedback_serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(feedback_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.data.get('user_id')
        try:
            user = UserTB.objects.get(userID=user_id)
        except UserTB.DoesNotExist:
            return Response({"error": "User ID not found."}, status=status.HTTP_400_BAD_REQUEST)

        feedback_serializer = FeedbackSerializer(data=request.data)
        if feedback_serializer.is_valid():
            feedback_serializer.save()
            return Response(feedback_serializer.data, status=status.HTTP_201_CREATED)
        return Response(feedback_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class FeedbackDeleteView(APIView):
#     def delete(self, request, pk):
#         try:
#             feedback = Feedback.objects.get(feedback_id=pk)
#         except Feedback.DoesNotExist:
#             return Response({"error": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

#         feedback.delete()
#         return Response({"message": f"Feedback {pk} deleted permanent."}, status=status.HTTP_204_NO_CONTENT)

"""Logs Handling...................................................."""
# View to capture logs

class UserActivityLogView(APIView):
    permission_classes=[IsAuthenticated]


    def post(self, request):
        user_id = request.data.get('userID')
        action = request.data.get('action')
        details = request.data.get('details')

        try:
            user = UserTB.objects.get(userID=user_id)
        except UserTB.DoesNotExist:
            return Response({"error": "Invalid userID"}, status=status.HTTP_400_BAD_REQUEST)

        log = UserActivityLog(userID=user, action=action, details=details)
        log.save()
        serializer = UserActivityLogSerializer(log)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        # Retrieve and return logs
        logs = UserActivityLog.objects.all()
        serializer = UserActivityLogSerializer(logs, many=True)
        
        return Response(serializer.data)
    
class NotificationUSER(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Retrieve all notifications for a specific user
        notifications = Notification_USER.objects.filter(user_id=user_id).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        # Create a new notification
        user_id = request.data.get('userID')  # Assuming this refers to an appointment ID
        notification_type = request.data.get('notification_type')  # Field name for notification type
        message_content = request.data.get('message_content')  # Field name for message content
        receiver_id = request.data.get('receiverID')

        # Retrieve the AppointmentsTB instance by user_id (which should actually be an appointment ID)
        appointment = get_object_or_404(AppointmentsTB, pk=user_id)

        # Create the notification
        notification = Notification_USER.objects.create(
            userID=appointment,  # Assign the appointment instance here
            notification_type=notification_type,
            message_content=message_content,
            receiverID=receiver_id
        )

        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, notification_id):
        # Update a specific notification
        notification = get_object_or_404(Notification_USER, pk=notification_id)
        read_status = request.data.get('read')

        if read_status is not None:
            notification.read = read_status
        notification.save()

        serializer = NotificationSerializer(notification)
        return Response({
            'message': 'The notification was updated successfully',
            'notificationID': notification.id
        }, status=status.HTTP_200_OK)

    def delete(self, request, notification_id):
        # Delete a specific notification
        notification = get_object_or_404(Notification_USER, pk=notification_id)
        notification.delete()
        return Response({
            'message': 'The notification was deleted successfully'
        }, status=status.HTTP_200_OK)