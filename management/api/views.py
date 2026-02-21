from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.views import APIView

from management.models import UserModel, Property, Lease, Announcement, MetersModel, BillModel
from .serializers import UserCreateSerializer, UserDetailSerializer, PropertySerializer, LeaseSerializer, AnnouncementDetailSerializer, AnnouncementCreateSerializer, AnnouncementDetailLandlordSerializer, MetersSerializer, BillSerializer, BillReadSerializer
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

    @action(detail=True, methods=['get'])
    def bills(self, request, pk):
        flat = self.get_object()
        bills = BillModel.objects.filter(lease__flat=flat)
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    # filtrowanie po  'username': ['iexact']
    filterset_class = UserFilter

    def get_queryset(self):
        if self.request.user.is_landlord:
            # Wyświetlanie tenantow danego landlorda
            return UserModel.objects.filter(tenant_leases__landlord=self.request.user).distinct()
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

    @action(detail=True, methods=["get"])
    def leases(self, request, pk):
        user = self.get_object()
        if user.is_landlord:
            serialzier = LeaseSerializer(
                Lease.objects.filter(landlord=user), many=True)
            return Response(serialzier.data)

        serialzier = LeaseSerializer(
            Lease.objects.filter(tenant=user), many=True)
        return Response(serialzier.data)


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


class AnnouncementModelViewSet(ModelViewSet):

    permission_classes = [LandlordCreatePermission]
    serializer_class = AnnouncementDetailSerializer
    queryset = Announcement.objects.all()

    def get_queryset(self):
        if self.request.user.is_landlord:
            return Announcement.objects.filter(sender=self.request.user)
        elif self.request.user.is_tenant:
            return Announcement.objects.filter(recipent=self.request.user)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return AnnouncementCreateSerializer
        elif self.request.user.is_landlord:
            return AnnouncementDetailLandlordSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MetersModelViewSet(ModelViewSet):
    serializer_class = MetersSerializer
    permission_classes = [LandlordCreatePermission]
    queryset = MetersModel.objects.all()

    def get_queryset(self):
        # Wyszukiwanie po roli usera <-dlatego może byc niewidoczne
        if self.request.user.is_landlord:
            return MetersModel.objects.filter(bill__lease__landlord=self.request.user)
        elif self.request.user.is_tenant:
            return MetersModel.objects.filter(bill__lease__tenant=self.request.user)
        return super().get_queryset()


class BillModelViewSet(ModelViewSet):
    serializer_class = BillReadSerializer
    permission_classes = [LandlordCreatePermission]

    queryset = BillModel.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return BillSerializer
        return super().get_serializer_class()
