from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Deposit
# from django.db.models.functions import Trunc
from django.db.models import DateTimeField, Sum, Min, Max

# Create your views here.


def index(request):
    # template = loader.get_template('finance/index.html')

    qs = Deposit.objects.all()

    # summary_over_time = qs.annotate(
    #     period=Trunc(
    #         'created',
    #         'day',
    #         output_field=DateTimeField
    #     ),
    # ).values('request_date')\
    #     .annotate(total=(Sum('amount')))\
    #     .order_by('request_date')
    #
    # summary_range = summary_over_time.aggregate(
    #     low=Min('total'),
    #     high=Max('total'),)
    #
    context = {}

    return render(request, 'finance/index.html', context)

