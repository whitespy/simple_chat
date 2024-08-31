from django_filters import rest_framework as filters

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ThreadFilter(filters.FilterSet):
    participant = filters.ModelChoiceFilter(
        lookup_expr="exact",
        field_name="participants",
        queryset=UserModel.objects.all(),
    )
