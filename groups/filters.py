from groups.models import Group
import django_filters

class GroupFilter(django_filters.FilterSet):
    class Meta:
        model=Group
        fields=['name','length','ppw','numplayers']