from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from properties.models import Room
from tenants.models import Tenant
from payments.models import Payment
import json

@login_required
def dashboard(request):
    total_rooms = Room.objects.count()
    total_tenants = Tenant.objects.count()
    income_data = Payment.objects.filter(status='PAID').aggregate(total=Sum('amount'))
    total_income = income_data['total'] or 0
    overdue_count = Payment.objects.filter(status='OVERDUE').count()
    pending_count = Payment.objects.filter(status='UNPAID').count()
    
    monthly_data = Payment.objects.filter(status='PAID').annotate(month=TruncMonth('paid_date')).values('month').annotate(total=Sum('amount')).order_by('month')
    labels, data = [], []
    for item in monthly_data:
        labels.append(item['month'].strftime('%b %Y'))
        data.append(float(item['total']))
        
    recent_payments = Payment.objects.select_related('tenant', 'tenant__room').order_by('-due_date')[:5]
    upcoming_dues = Payment.objects.filter(status__in=['UNPAID', 'OVERDUE']).select_related('tenant', 'tenant__room').order_by('due_date')[:5]
        
    context = {
        'total_rooms': total_rooms, 
        'total_tenants': total_tenants, 
        'total_income': total_income,
        'overdue_count': overdue_count,
        'pending_count': pending_count, 
        'chart_labels': json.dumps(labels), 
        'chart_data': json.dumps(data),
        'recent_payments': recent_payments, 
        'upcoming_dues': upcoming_dues,
    }
    return render(request, 'core/dashboard.html', context)