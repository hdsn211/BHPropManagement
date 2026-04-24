from payments.models import Inquiry, MaintenanceTicket

def notification_counts(request):
    return {
        'unread_inquiries_count': Inquiry.objects.filter(status='PENDING').count(),
        'unread_maintenance_count': MaintenanceTicket.objects.exclude(status='RESOLVED').count(),
    }