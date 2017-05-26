from django.test import TestCase
from .models import Credit, Capital, Fund
from django.contrib.auth.admin import User
from django.contrib import auth
from django.utils import timezone
from django.db.models import F, FloatField, Sum

# Create your tests here.


class CreditTest(TestCase):

    def setUp(self):
        self.client
        member1 = User.objects.create_user(username='test1', email='test@test.com', password='test1@2017')
        member2 = User.objects.create_user(username='test2', email='test2@test.com', password='test2@2017')
        member3 = User.objects.create_user(username='test3', email='test2@test.com', password='test3@2017')  # treasurer

        member1.has_perm(perm='can_add_credit', obj=Credit)
        member2.has_perm(perm='can_add_credit', obj=Credit)

        Credit.objects.create(creditor=member1, amount=200000, repayment_date=timezone.now().date(), guarantor=member1)
        Capital.objects.create(owner=member1, share_capital=10000, deposit_date=timezone.now())
        Capital.objects.create(owner=member1, share_capital=20000, deposit_date=timezone.now())
        Capital.objects.create(owner=member2, share_capital=15000, deposit_date=timezone.now())

        count = Capital.objects.count()
        self.assertEquals(count, 3)
        print(Capital.objects.all().aggregate(total=Sum(F('share_capital'))))

    def test_user_capital(self):
        c = self.client
        c.login(username='test1', password='test1@2017')
        user = auth.get_user(self.client)
        assert user.is_authenticated

        print(Capital.objects.filter(owner=user).aggregate(total=Sum(F('share_capital'))))








