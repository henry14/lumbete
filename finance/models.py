from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Credit(models.Model):
    creditor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    request_date = models.DateTimeField(auto_now=True)
    repayment_date = models.DateField('Date of Repayment')
    guarantor = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related", on_delete=None)
    approved = models.BooleanField(default=False)


# idea: Member inputs their deposit & treasurer approves
class Fund(models.Model):  # Show total amount saved
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    deposit_date = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)


# Assumption: interest is earned on share capital
class Capital(models.Model):  # Show total share capital and interest earned
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    share_capital = models.PositiveIntegerField(default=0)
    deposit_date = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)


class Approval(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)