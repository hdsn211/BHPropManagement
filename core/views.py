from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from properties.models import Room, Property
from tenants.models import Tenant
from payments.models import Payment
import json

@login_required
def dashboard(request):
    # SECURITY CHECK 
    # Superuser can only enter admin page
    if not request.user.is_superuser:
        # If not a superuser check if they are an OWNER
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'OWNER':
            return redirect('/tenant-portal/') 
    
    # New Property Stats
    total_properties = Property.objects.count()
    total_rooms = Room.objects.count()
    total_tenants = Tenant.objects.count()
    
    occupied_units = Room.objects.filter(is_occupied=True).count()
    vacant_units = Room.objects.filter(is_occupied=False).count()
    occupancy_rate = (occupied_units / total_rooms * 100) if total_rooms > 0 else 0
    vacant_rate = round(100.0 - occupancy_rate, 1)

    income_data = Payment.objects.filter(status='PAID').aggregate(total=Sum('amount'))
    total_income = income_data['total'] or 0
    overdue_count = Payment.objects.filter(status='OVERDUE').count()
    pending_count = Payment.objects.filter(status='UNPAID').count()

    # New Unit Types Data
    unit_types_raw = Room.objects.values('property__property_type').annotate(count=Count('id')).order_by('-count')
    unit_types = []
    for item in unit_types_raw:
        percentage = (item['count'] / total_rooms * 100) if total_rooms > 0 else 0
        unit_types.append({
            'type': item['property__property_type'],
            'count': item['count'],
            'percentage': round(percentage)
        })

    # Chart Data
    monthly_data = (
        Payment.objects.filter(status='PAID')
        .annotate(month=TruncMonth('paid_date'))
        .values('month').annotate(total=Sum('amount'))
        .order_by('month')
    )
    labels, data = [], []
    for item in monthly_data:
        labels.append(item['month'].strftime('%b %Y'))
        data.append(float(item['total']))
        
    recent_payments = Payment.objects.select_related('tenant', 'tenant__room').order_by('-due_date')[:5]
        
    context = {
        'total_properties': total_properties,
        'total_rooms': total_rooms,
        'total_tenants': total_tenants,
        'occupied_units': occupied_units,
        'vacant_units': vacant_units,
        'occupancy_rate': round(occupancy_rate, 1),
        'vacant_rate': vacant_rate,
        'total_income': total_income,
        'overdue_count': overdue_count,
        'pending_count': pending_count,
        'unit_types': unit_types,
        'chart_labels': json.dumps(labels), 
        'chart_data': json.dumps(data),
        'recent_payments': recent_payments, 
    }
    return render(request, 'core/dashboard.html', context)