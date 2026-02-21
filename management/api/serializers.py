

from management.models import UserModel, Property, Lease, Announcement, MetersModel, BillModel

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.db.models import Q
from decimal import Decimal


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["username", 'last_name', 'email', 'is_landlord',
                  'is_tenant', 'phone', 'password']

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "username", 'last_name', 'email', 'is_landlord',
                  'is_tenant', 'phone']


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = '__all__'


class LeaseSerializer(serializers.ModelSerializer):
    deposit = serializers.DecimalField(
        max_digits=8, decimal_places=2, read_only=True)

    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        flat = attrs.get('flat')
        qs = Lease.objects.filter(flat=flat)
        if start and end:
            overlapping = qs.filter(
                Q(start_date__lt=end) & Q(end_date__gt=start)).exists()
            if overlapping:
                raise ValidationError(
                    {'date_conflict': 'Lease overlaps with existing lease'})
        return attrs

    class Meta:
        model = Lease
        fields = '__all__'

    def create(self, validated_data):
        validated_data["deposit"] = 3 * validated_data["rent_amount"]
        return super().create(validated_data)


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    sender = UserCreateSerializer(read_only=True)

    class Meta:
        model = Announcement
        exclude = ['recipient']


class AnnouncementDetailLandlordSerializer(serializers.ModelSerializer):
    recipient = UserCreateSerializer(read_only=True, many=True)

    class Meta:
        model = Announcement
        exclude = ['sender']


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    recipient = serializers.PrimaryKeyRelatedField(
        many=True, queryset=UserModel.objects.all())

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'created_at', 'recipient']


class MetersSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetersModel
        exclude = ["bill"]


class BillSerializer(serializers.ModelSerializer):
    meters_data = MetersSerializer(
        write_only=True, required=False, allow_null=True)

    def validate(self, attrs):

        meters_data = attrs.get('meters_data')

        if not meters_data:
            raise ValidationError('Provide data: meters_data')

        return super().validate(attrs)

    class Meta:
        model = BillModel
        fields = ["lease", 'date', 'rent_amount',
                  'is_paid', 'meters_data']

    def create(self, validated_data):

        meters_data = validated_data.pop("meters_data")
        utilities = (
            Decimal(meters_data.get("gas", 0)) +
            Decimal(meters_data.get("heat", 0)) +
            Decimal(meters_data.get("electricity", 0)) +
            Decimal(meters_data.get("water", 0))
        )
        validated_data['utilities_amount'] = utilities + \
            validated_data['rent_amount']
        bill = BillModel.objects.create(**validated_data)
        MetersModel.objects.create(bill=bill, **meters_data)
        return bill

    def update(self, instance, validated_data):
        meters_data = validated_data.pop("meters_data")

        meters_instance = instance.meters

        for atr, val in meters_data.items():
            setattr(meters_instance, atr, val)

        meters_instance.save()

        for atr, val in validated_data.items():
            setattr(instance, atr, val)
        instance.save()
        return instance


class BillReadSerializer(serializers.ModelSerializer):
    meters = MetersSerializer()

    class Meta:
        model = BillModel
        fields = '__all__'
