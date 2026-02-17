from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser

from management.models import UserModel, Property
from .serializers import UserCreateSerializer, UserDetailSerializer, PropertySerializer


class PropertyModelViewSet(ModelViewSet):
    model = Property
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_tenant == True:
            return Property.objects.filter(id=self.request.user.id)

        return super().get_queryset()

    def get_permissions(self):
        if self.action == "create":
            return [IsAdminUser()]
        return super().get_permissions()


class UserModelViewSet(ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_landlord == True:
            return UserModel.objects.all()

        return UserModel.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserDetailSerializer

        return UserCreateSerializer

    @action(methods=["GET"], detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    


