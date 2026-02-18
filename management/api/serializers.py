from management.models import UserModel, Property, Lease

from rest_framework import serializers


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
        fields = ["username", 'last_name', 'email', 'is_landlord',
                  'is_tenant', 'phone']


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = '__all__'


class LeaseSerializer(serializers.ModelSerializer):
    tenant = UserDetailSerializer(read_only=True)

    class Meta:
        model = Lease
        fields = '__all__'
