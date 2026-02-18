from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView

from management.models import UserModel, Property, Lease
from .serializers import UserCreateSerializer, UserDetailSerializer, PropertySerializer, LeaseSerializer
from .permissions import LandlordPermission
from .filters import UserFilter


class PropertyModelViewSet(ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [LandlordPermission]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        if self.request.user.is_tenant == True:
            return Property.objects.filter(leases__tenant=self.request.user)

        return super().get_queryset()


class UserModelViewSet(ModelViewSet):
    filterset_class = UserFilter
    permission_classes = [LandlordPermission]

    def get_queryset(self):
        if self.request.user.is_landlord == True:
            return UserModel.objects.all()

        return UserModel.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserDetailSerializer

        return UserCreateSerializer

    @action(methods=["GET"], detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class LeaseModelViewSet(ModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer
    permission_classes = [LandlordPermission]

    def get_queryset(self):
        if self.request.user.is_tenant == True:
            return Lease.objects.filter(id=self.request.user.id)
        return super().get_queryset()


class RegisterApiView(APIView):
    

    def post(self, request):

        serializer = UserCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
