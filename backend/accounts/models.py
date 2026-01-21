from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from branch.models import Branch

# Create your models here.
class MembershipType(models.Model):
    MEMBER_TYPES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('public', 'Public'),
        ('corporate', 'Corporate'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=MEMBER_TYPES)
    max_books = models.IntegerField(default=5)
    loan_period_days = models.IntegerField(default=14)
    max_renewals = models.IntegerField(default=2)
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fine_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    member_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='member_photos/', null=True, blank=True)
    barcode = models.CharField(max_length=100, unique=True)
    membership_type = models.ForeignKey(MembershipType, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    registration_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.member_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_membership_valid(self):
        return self.is_active and self.expiry_date >= timezone.now().date()

