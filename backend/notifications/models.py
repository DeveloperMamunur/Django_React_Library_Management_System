from django.db import models
from accounts.models import Member

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('overdue', 'Overdue Item'),
        ('due_soon', 'Due Soon'),
        ('reserved', 'Reserved Item Available'),
        ('expiry', 'Membership Expiry'),
        ('fine', 'Fine Notice'),
    ]
    
    DELIVERY_METHODS = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHODS)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.notification_type} - {self.member.member_id}"