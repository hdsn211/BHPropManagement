from datetime import date
from django.db import models

class Payment(models.Model):
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PAID_LATE', 'Paid Late'),
        ('OVERDUE', 'Overdue'),
        ('UNPAID', 'Pending')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNPAID')

    def save(self, *args, **kwargs):
        today = date.today()
        if self.paid_date:
            if self.paid_date > self.due_date:
                self.status = 'PAID_LATE'
            else:
                self.status = 'PAID'
        elif today > self.due_date:
            self.status = 'OVERDUE'
        else:
            self.status = 'UNPAID'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tenant.name} - {self.status}"

class Inquiry(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('READ', 'Read'),
        ('RESOLVED', 'Resolved'),
    ]

    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey('properties.Room', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Inquiry from {self.name}"
    
class MaintenanceTicket(models.Model):
    CATEGORY_CHOICES = [
        ('PLUMBING', 'Plumbing'),
        ('ELECTRICAL', 'Electrical'),
        ('FURNITURE', 'Furniture'),
        ('CLEANING', 'Cleaning'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE)
    room = models.ForeignKey('properties.Room', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    description = models.TextField()
    image = models.ImageField(upload_to='maintenance_photos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.status}] {self.category} - {self.room.name}"