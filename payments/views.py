from .models import Payment, Inquiry, MaintenanceTicket
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PaymentForm, InquiryForm, MaintenanceForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from tenants.models import Tenant
from .models import Payment, Inquiry
from .forms import PaymentForm, InquiryForm
from properties.models import Property, Room
import calendar
from datetime import date
import json


# --- PUBLIC VIEW ---
def submit_inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            room_id = request.POST.get('room_id')
            property_id = request.POST.get('property_id')
            inquiry = form.save(commit=False)
            if room_id:
                inquiry.room = Room.objects.get(id=room_id)
                inquiry.property = Property.objects.get(id=property_id)
            inquiry.save()
            messages.success(request, "Your inquiry has been sent successfully!")
            return redirect('public_room_list', property_id=property_id)
    return redirect('public_home')

# --- ADMIN CRUD VIEWS ---
@login_required
def payment_list(request):
    payments = Payment.objects.select_related('tenant', 'tenant__room').all()
    q = request.GET.get('q')
    status_filter = request.GET.get('status')
    if q:
        payments = payments.filter(tenant__name__icontains=q)
    if status_filter:
        payments = payments.filter(status=status_filter)
    status_choices = Payment.STATUS_CHOICES
    
    paginator = Paginator(payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'payments': payments, 'q': q or '', 'status_filter': status_filter or '', 
        'status_choices': status_choices, 'page_obj': page_obj
    }
    return render(request, 'payments/payment_list.html', context)

def add_payment(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('payment_list')
    return render(request, 'payments/payment_form.html', {'form': form})

def edit_payment(request, id):
    payment = Payment.objects.get(id=id)
    form = PaymentForm(request.POST or None, instance=payment)
    if form.is_valid():
        form.save()
        return redirect('payment_list')
    return render(request, 'payments/payment_form.html', {'form': form})

@login_required
def delete_payment(request, id):
    payment = Payment.objects.get(id=id)
    payment.delete()
    return redirect('payment_list')

@login_required
def inquiry_list(request):
    inquiries = Inquiry.objects.select_related('room', 'property').order_by('-created_at')
    inquiries.update(is_read=True)
    return render(request, 'payments/inquiry_list.html', {'inquiries': inquiries})

@login_required
def generate_dues(request):
    if request.method == 'POST':
        today = timezone.now().date()
        year, month = today.year, today.month
        due_day = 5
        try:
            due_date = date(year, month, due_day)
        except ValueError:
            last_day = calendar.monthrange(year, month)[1]
            due_date = date(year, month, last_day)

        active_tenants = Tenant.objects.filter(room__isnull=False, room__is_occupied=True)
        created_count = 0
        for tenant in active_tenants:
            exists = Payment.objects.filter(tenant=tenant, due_date__year=year, due_date__month=month).exists()
            if not exists:
                Payment.objects.create(tenant=tenant, amount=tenant.room.rent_amount, due_date=due_date, status='UNPAID')
                created_count += 1

        if created_count > 0:
            messages.success(request, f'Successfully generated {created_count} payment records.')
        else:
            messages.warning(request, f'No new payments generated.')
    return redirect('dashboard')

@login_required
def maintenance_list(request):
    tickets = MaintenanceTicket.objects.select_related('tenant', 'room').order_by('-created_at')
    return render(request, 'payments/maintenance_list.html', {'tickets': tickets})

@login_required
def update_maintenance_status(request, id):
    ticket = get_object_or_404(MaintenanceTicket, id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(MaintenanceTicket.STATUS_CHOICES).keys():
            ticket.status = new_status
            ticket.save()
    return redirect('maintenance_list')