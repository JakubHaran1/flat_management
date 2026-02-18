from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.views import APIView

from management.models import UserModel, Property, Lease
from .serializers import UserCreateSerializer, UserDetailSerializer, PropertySerializer, LeaseSerializer
from .permissions import LandlordCreatePermission
from .filters import UserFilter


class PropertyModelViewSet(ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [LandlordCreatePermission]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        if self.request.user.is_tenant == True:
            return Property.objects.filter(leases__tenant=self.request.user)
        elif self.request.user.is_landlord == True:
            return Property.objects.filter(leases__landlord=self.request.user)

        return super().get_queryset()


class UserModelViewSet(ModelViewSet):
    # filtrowanie po  'username': ['iexact']
    filterset_class = UserFilter

    def get_queryset(self):
        if self.request.user.is_landlord:
            # Wyświetlanie tenantow danego landlorda
            return UserModel.objects.filter(tenant_leases__landlord=self.request.user)
        elif self.request.user.IsAdminUser:
            return UserModel.objects.all()

        return UserModel.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj == request.user:
            raise PermissionDenied("You can't edit other user")

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj == request.user:
            raise PermissionDenied("You can't edit other user")
        return super().partial_update(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserDetailSerializer

        return UserCreateSerializer


class LeaseModelViewSet(ModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer

    # tylko landlord moze tworzyc/edytowac umowy
    permission_classes = [LandlordCreatePermission]

    def get_queryset(self):
        if self.request.user.is_tenant == True:
            return Lease.objects.filter(tenant=self.request.user)
        elif self.request.user.is_landlord == True:
            return Lease.objects.filter(landlord=self.request.user)
        return super().get_queryset()


class RegisterApiView(APIView):

    def post(self, request):

        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
