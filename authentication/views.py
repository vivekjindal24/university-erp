from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from google.auth.transport import requests
from google.oauth2 import id_token
from django.conf import settings
import json
from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserProfileSerializer, ChangePasswordSerializer
)
from django.shortcuts import render

class UserRegistrationView(generics.CreateAPIView):
    """User Registration API View"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User Login API View"""
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)

    return Response({
        'user': UserSerializer(user).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    })

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def google_login_view(request):
    """Google OAuth Login API View"""
    try:
        # Get the Google ID token from the request
        google_token = request.data.get('token')
        user_type = request.data.get('user_type', 'student')  # Default to student

        if not google_token:
            return Response({'error': 'Google token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the Google ID token
        try:
            idinfo = id_token.verify_oauth2_token(google_token, requests.Request())

            # Check if the token is from Google
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # Get user information from Google
            google_user_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name', '')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            picture = idinfo.get('picture', '')

        except ValueError:
            return Response({'error': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        try:
            user = User.objects.get(email=email)
            created = False
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]  # Use email prefix as username

            # Make sure username is unique
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                is_active=True
            )

            # Create user profile
            UserProfile.objects.create(
                user=user,
                bio=f"Registered via Google OAuth"
            )

            created = True

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'created': created,
            'message': 'User created successfully' if created else 'User logged in successfully'
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    """User Logout API View"""
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """User Profile API View"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """Change Password API View"""
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    old_password = serializer.validated_data['old_password']
    new_password = serializer.validated_data['new_password']

    if not user.check_password(old_password):
        return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    """User List API View (for admin)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        user_type = self.request.query_params.get('user_type', None)
        if user_type is not None:
            queryset = queryset.filter(user_type=user_type)
        return queryset

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def google_login_test_view(request):
    """Google OAuth Test Page"""
    return render(request, 'auth/google_login_test.html')
