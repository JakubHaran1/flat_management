
import django_filters
from management.models import UserModel, Lease


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = UserModel
        fields = {
            'username': ['iexact']
        }


class LeaseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='start_date__date')

    class Meta:
        model = Lease
        fields = {
            'start_date': ['lt', 'gt', 'range']
        }
