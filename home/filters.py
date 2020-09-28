import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class AppoinmentFilter(django_filters.FilterSet):

	end_date = DateFilter(field_name="date_created", lookup_expr='lte')

	class Meta:
		model = Appoinment
		fields = '__all__'
		exclude = ['patient', 'date_created']