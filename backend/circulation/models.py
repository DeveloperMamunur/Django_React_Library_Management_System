from django.db import models
from django.contrib.auth.models import User
from catalog.models import Item, Copy
from accounts.models import Member
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('checkout', 'Check Out'),
        ('checkin', 'Check In'),
        ('renew', 'Renew'),
        ('reserve', 'Reserve'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='transactions')
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    renewed_count = models.IntegerField(default=0)
    staff_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions_processed')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.transaction_type} - {self.member.member_id} - {self.copy.barcode}"
    
    @property
    def is_overdue(self):
        if self.due_date and not self.return_date:
            return timezone.now().date() > self.due_date
        return False
    
    @property
    def days_overdue(self):
        if self.is_overdue:
            return (timezone.now().date() - self.due_date).days
        return 0


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('available', 'Available'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reservations')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    available_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    fulfilled_date = models.DateField(null=True, blank=True)
    notified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.member.member_id} - {self.item.title}"


class Fine(models.Model):
    FINE_TYPES = [
        ('overdue', 'Overdue Fine'),
        ('lost', 'Lost Item'),
        ('damaged', 'Damaged Item'),
        ('membership', 'Membership Fee'),
        ('other', 'Other'),
    ]
    
    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='fines')
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    fine_type = models.CharField(max_length=20, choices=FINE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.member.member_id} - {self.fine_type} - ${self.amount}"
    
    @property
    def balance(self):
        return self.amount - self.amount_paid


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('online', 'Online Payment'),
        ('check', 'Check'),
        ('other', 'Other'),
    ]
    
    fine = models.ForeignKey(Fine, on_delete=models.CASCADE, related_name='payments')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    receipt_number = models.CharField(max_length=100, unique=True)
    staff_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.receipt_number} - ${self.amount}"

