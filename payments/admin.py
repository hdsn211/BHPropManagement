from django.contrib import admin
from .models import Payment, Inquiry, MaintenanceTicket

@admin.register(MaintenanceTicket)
class MaintenanceTicketAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'room', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
# Register your models here.
