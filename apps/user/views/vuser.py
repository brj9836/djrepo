"""
Edicion de usuarios
"""

# standard library
from typing import Union

from django.contrib.auth.models import User

# Django
from django.http import Http404

# third-party
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

# local Django
from apps.user.serializers import (
    UserHeavySerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class VUserList(APIView):
    """
    ...
    """

    permission_classes = (IsAdminUser,)
    serializer = UserHeavySerializer

    def serialize_user(self, pk):
        """
        ...
        """
        try:
            user = User.objects.get(pk=pk)
            res = self.serializer(user)
            return res.data
        except User.DoesNotExist:  # pragma: no cover
            raise Http404

    def get(self, request, format=None):
        """
        ...
        """
        response = self.serializer(User.objects.all().order_by("id"), many=True,)
        return Response(response.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        ...
        """
        response = UserRegisterSerializer(data=request.data)
        if response.is_valid():
            iduser: int = response.save()
            res = self.serialize_user(pk=iduser)
            return Response(res, status=status.HTTP_201_CREATED)

        return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)


class VUserDetail(APIView):
    """
    ...
    """

    permission_classes = (IsAdminUser,)
    serializer = UserSerializer

    def get_object(self, pk_user: Union[int, str]):
        """
        ...
        """
        try:
            return User.objects.get(pk=pk_user)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk: Union[int, str], format=None):
        """
        ...
        """
        user = self.get_object(pk)
        response = UserHeavySerializer(user)
        return Response(response.data, status=status.HTTP_200_OK)

    def put(self, request, pk: Union[int, str], format=None):
        """
        ...
        """
        user = self.get_object(pk)
        response = self.serializer(user, data=request.data)
        if response.is_valid():
            result = response.save()
            res = UserHeavySerializer(result)
            return Response(res.data, status=status.HTTP_200_OK)

        return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: Union[int, str], format=None):
        """
        ...
        """
        user = self.get_object(pk)

        if user.id == request.user.id:
            return Response("can't delete himself", status=status.HTTP_400_BAD_REQUEST,)

        if user.is_superuser:
            return Response(
                "super users cannot be deleted", status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_staff:
            if not request.user.is_superuser:
                return Response(
                    "user cannot delete administrators",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
