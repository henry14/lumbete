from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import User
from .models import Deposit, Loan, Capital, LoanSummary, CapitalSummary, DepositSummary
# from django.db.models.functions import Trunc
from django.db.models import Count, Sum, Min, Max, DateTimeField

# Register your models here.

# admin.autodiscover()
admin.site.site_header = 'Finance Administration'
admin.site.site_title = 'Finance'


def compute_reduction(mdebit, mcredit):

    if mdebit is None or mdebit < mcredit:
        per_paid = 100
    else:
        if mcredit is None:
            per_paid = 0
        else:
            per_paid = mcredit / float(mdebit) * 100

    return per_paid


@admin.register(LoanSummary)
class LoanSummaryAdmin(ModelAdmin):
    change_list_template = 'finance/loan_summary_change_list.html'

    def changelist_view(self, request, extra_context=None):
        response = super(LoanSummaryAdmin, self).changelist_view(request, extra_context)

        qs = User.objects.annotate(total_debit=Sum('deposit__amount'),
                                   paid=Sum('loan__amount'))
        dlist = []
        for x in qs:
            y = compute_reduction(x.total_debit, x.paid)

            dlist.append({'user':x.username, 'credit': x.paid, 'debit': x.total_debit, 'reduction': y})

        # response.context_data['summary'] = list(qs.order_by('debit__amount'))
        response.context_data['summary'] = list(dlist)

        return response


@admin.register(CapitalSummary)
class CaptalSummary(ModelAdmin):
    change_list_template = 'finance/capital_summary_change_list.html'


@admin.register(DepositSummary)
class LoanSummary(ModelAdmin):
    change_list_template = 'finance/deposit_summary_change_list.html'

    # def changelist_view(self, request, extra_context=None):
    #     response = super().changelist_view(
    #         request, extra_context,
    #     )
    #     try:
    #         qs = response.context_data['c1'].queryset
    #     except (AttributeError, KeyError):
    #         return response
    #
    #     summary_over_time = qs.annotate(
    #         period=Trunc(
    #             'created',
    #             'day',
    #             output_field=DateTimeField
    #         ),
    #     ).values('request_date')\
    #         .annotate(total=(Sum('amount')))\
    #         .order_by('request_date')
    #
    #     summary_range = summary_over_time.aggregate(
    #         low=Min('total'),
    #         high=Max('total'),)
    #
    #     high = summary_range.get('high', 0)
    #     low = summary_range.get('low', 0)
    #     response.context_data['summary_over_time'] = [{
    #         'period': x['period'],
    #         'total': x['total'] or 0,
    #         'pct': ((x['total'] or 0) - low) / (high - low) * 100
    #         if high > low else 0,
    #     } for x in summary_over_time]
    #
    #     return response


class FinanceAdminSite(AdminSite):
    site_header = 'Finance Administration'
    # index_template = "admin/finance/index.html"

# admin_site = FinanceAdminSite(name="finance")

# admin_site.register(Credit)
# admin_site.register(Fund)
# admin_site.register(Capital)


class LoanAdmin(admin.ModelAdmin):
    pass
    # fields = ["creditor"]
    # list_display = ['creditor']

#     def index(self, request, extra_context=None):
#         if User.get_username() == "finance17":
#             self.register(Capital)
#
#         return super(CreditAdmin, self).index(request, extra_context)

m_credit = FinanceAdminSite(name='testing finance')

# m_credit.register(Credit, CreditAdmin)

m_credit.register(Loan, LoanAdmin)
admin.site.register(Deposit)
admin.site.register(Loan)
admin.site.register(Capital)


