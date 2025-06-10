from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from .serializers import RegisterSerializer, UserProfileSerializer, ChangePasswordSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response




class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer 
    permission_classes = [IsAuthenticated]
    

    def get_object(self):
        return self.request.user
    

class UpdateUserProfileView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user




class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
