from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .serializers import *
from .models import *
# Create your views here.


class registrationAPIView(generics.CreateAPIView):
    serializer_class = Users_Serializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():

                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                user_serializer = Users_Serializer(user)

                return Response({
                    'message': 'User registered successfully',
                    'status': "Success",
                    'data': {
                        'user': user_serializer.data,
                        "accessToken": str(refresh.access_token),
                        'refreshToken': str(refresh)
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            error_messages = dict(e)
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)


class loginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        user = Users.objects.filter(
            phone_number=phone_number, is_active=True)

        if user.exists():
            # authenticated
            auth_user = authenticate(
                phone_number=user.first().phone_number, password=password)

            if auth_user:
                refresh = RefreshToken.for_user(auth_user)
                user_data = {
                    "id": auth_user.id,
                    "phone_number": auth_user.phone_number,
                    "is_superuser": auth_user.is_superuser,
                    "is_active": auth_user.is_active
                }

                return Response({
                    'message': 'User login successfully',
                    'status': 'Success',
                    'data': {
                        'user': user_data,
                        "accessToken": str(refresh.access_token),
                        'refreshToken': str(refresh)
                    }

                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "fullname or password is not correct"}, status=status.HTTP_401_UNAUTHORIZED)


class getNewTokenAPIView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                decoded_token = RefreshToken(refresh_token)
                user_id = decoded_token.payload.get("user_id")
                if user_id:
                    user = Users.objects.get(id=user_id)
                    new_access_token = str(decoded_token.access_token)
                    new_refresh_token = str(RefreshToken.for_user(user))
                    return Response({
                        "message": "Tokens successfull created",
                        "status": 'Success',
                        'data': {
                            'accessToken': new_access_token,
                            'refreshToken': new_refresh_token,
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'User ID not found in token', "status": "Failed"}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({'message': 'Invalid or expired refresh token', "status": "Failed"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Refresh token is required', 'status': "Failed"}, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = Users_Serializer


class UserDetailsAPIView(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = Users_Serializer


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = Users_Serializer


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = Users_Serializer


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data["new_password"]

            if not user.check_password(old_password):
                return Response(
                    {'message': "Incorrect old password",
                     "status": 'Failed'},
                    status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'message': "Password changed successfull", "status": "Success"}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
