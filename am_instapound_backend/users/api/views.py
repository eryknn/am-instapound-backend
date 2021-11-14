from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from am_instapound_backend.users.api.serializers import RegistrationSerializer, UserProfileSerializer

User = get_user_model()


class UserViewSet(GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    def get_object(self):
        return self.queryset.filter(id=self.request.user.id).get()

    @action(detail=False, methods=["GET", "PUT"], url_path='profile')
    def profile(self, request: Request):
        if request.method == 'GET':
            return self.__get_profile(request)

        return self.__update_profile(request)

    def __get_profile(self, request):
        serializer = self.get_serializer(self.get_object(), context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def __update_profile(self, request: Request):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
