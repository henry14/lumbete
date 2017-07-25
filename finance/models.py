from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.


# Amount one owes the cooperation
class Loan(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)  # Loan
    request_date = models.DateField(auto_now_add=True, editable=False)  # Date of loan request
    repayment_date = models.DateField('Date of Repayment')  # Date before which it has to be fully settled
    guarantor = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related", on_delete=None)

    class Meta:
        verbose_name_plural = 'Credit'

    def reduction(self):
        return self.amount - Deposit.objects.filter(owner__capital=self.requester)\
            .filter(owner__fund__repayment=True).aggregate(balance=Sum('amount'))

    def __str__(self):
        return "%s" %(self.creditor.get_username())


# idea: Member inputs their deposit & treasurer approves
class Deposit(models.Model):  # Show total amount saved
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    received_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related", on_delete=models.CASCADE)
    deposit_date = models.DateField(auto_now_add=True, editable=False)
    repayment = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s %s" % (self.owner.get_username(), self.amount, self.deposit_date)


# Assumption: interest is earned on share capital
class Capital(models.Model):  # Show total share capital and interest earned
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    share_capital = models.PositiveIntegerField(default=0)
    deposit_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = 'Capital'

    def __str__(self):
        return "%s %s %s" % (self.owner.get_username(), self.share_capital, self.deposit_date)


class DepositApproval(models.Model):
    deposit_approval = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, editable=False)


class LoanApproval(models.Model):
    loan_approval = models.ForeignKey(Loan, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, editable=False)


class DepositSummary(Deposit):
    # Compute amount  per month & total amount. Only those approved.
    class Meta:
        proxy = True
        verbose_name = 'Deposit Summary'
        verbose_name_plural = 'Deposit Summary'


class LoanSummary(Loan):
    # Compute amount  per month & total amount. Only those approved.
    class Meta:
        proxy = True
        verbose_name = 'Loan'
        verbose_name_plural = 'Loan Summary'


class CapitalSummary(Capital):
    class Meta:
        proxy = True
        verbose_name = 'Capital'
        verbose_name_plural = 'Capital Summary'

