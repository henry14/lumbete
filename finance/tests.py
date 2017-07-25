from django.test import TestCase
from .models import Debit, Capital, Fund, DebitSummary
from django.contrib.auth.admin import User
from django.contrib import auth
from django.utils import timezone
from django.db.models import F, FloatField, Sum
from .admin import CreditSummaryAdmin
from datetime import date, timedelta
from . import admin

# Create your tests here.


class CreditTest(TestCase):

    def setUp(self):
        self.client
        member1 = User.objects.create_user(username='test1', email='test@test.com', password='test1@2017')
        member2 = User.objects.create_user(username='test2', email='test2@test.com', password='test2@2017')
        member3 = User.objects.create_user(username='test3', email='test3@test.com', password='test3@2017')  # treasurer
        member4 = User.objects.create_user(username='test4', email='test4@test.com', password='test4@2017')

        member4.has_perm(perm='can_add_credit', obj=Debit)
        member3.has_perm(perm='can_add_credit', obj=Debit)

        Debit.objects.create(requester=member4, amount=400000,
                              repayment_date=date.today() + timedelta(7), guarantor=member3)
        Debit.objects.create(requester=member3, amount=700000,
                             repayment_date=date.today() + timedelta(2), guarantor=member1)
        Debit.objects.create(requester=member1, amount=300000,
                             repayment_date=date.today() + timedelta(5), guarantor=member2)
        # Credit.objects.create(creditor=member1, amount=50000,
        #                       repayment_date=date.today() - timedelta(6), guarantor=member2)

        Fund.objects.create(owner=member4, amount=100000,
                            deposit_date=date.today() - timedelta(4), repayment=True)
        Fund.objects.create(owner=member2, amount=300000,
                            deposit_date=date.today() - timedelta(3), repayment=False)

        Capital.objects.create(owner=member4, share_capital=10000, deposit_date=timezone.now())
        Capital.objects.create(owner=member4, share_capital=20000, deposit_date=timezone.now())
        Capital.objects.create(owner=member3, share_capital=15000, deposit_date=timezone.now())

        # DebitSummary.objects.create(requester=member3, amount=60000, repayment_date=timezone.now().date(),
        #                              guarantor=member4)
        count = Capital.objects.count()
        self.assertEquals(count, 3)
        # print(Capital.objects.all().aggregate(total=Sum(F('share_capital'))))

    def test_user_capital(self):
        c = self.client
        c.login(username='test4', password='test4@2017')
        user = auth.get_user(self.client)
        assert user.is_authenticated

        print(Capital.objects.filter(owner=user).aggregate(total=Sum(F('share_capital'))))

    def test_credit_summary(self):
        self.client
        nums = list(User.objects.annotate(total_debit=Sum('debit__amount'), paid=Sum('fund__amount')))

        self.assertEqual(nums.__len__(), 4, 'More than three users exist')

        num4 = nums.__getitem__(1)
        num3 = nums.__getitem__(0)
        num1 = nums.__getitem__(2)
        num2 = nums.__getitem__(3)
        print(num3, num3.total_debit, num3.paid)

        self.assertEqual(admin.compute_reduction(num4.total_debit, num4.paid), 25)
        self.assertEqual(admin.compute_reduction(num3.total_debit, num3.paid), 0)
        self.assertEqual(admin.compute_reduction(num2.total_debit, num2.paid), 100)
        self.assertEqual(admin.compute_reduction(num1.total_debit, num1.paid), 0)

        # for num in nums:
        #     print(num.get_username(), num.total_credit, num.reducing_bal)

        # print(CreditSummaryAdmin.changelist_view(test_credit)












