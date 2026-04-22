from django.contrib import admin
from properties.models import Property, Room
from tenants.models import Tenant, Profile
from payments.models import Payment, Inquiry

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_type', 'address')
    list_filter = ('property_type',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'property', 'rent_amount', 'is_occupied')
    list_filter = ('property', 'is_occupied')

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'contact', 'start_date')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'room')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'amount', 'due_date', 'status')
    list_filter = ('status',)

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'contact_number', 'created_at', 'is_read')
    list_filter = ('is_read',)