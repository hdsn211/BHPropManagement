from payments.models import Payment, MaintenanceTicket
from payments.forms import PaymentForm, InquiryForm, MaintenanceForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import Tenant, Profile
from .forms import TenantForm
from properties.models import Room
from payments.models import Payment
from django.contrib import messages
from django.core.paginator import Paginator

# --- HELPER FUNCTION ---
def update_room_occupancy(room):
    if room is not None:
        has_tenants = Tenant.objects.filter(room=room).exists()
        room.is_occupied = has_tenants
        room.save()

# --- AUTHENTICATION ---
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        try:
            if self.request.user.profile.role == 'OWNER':
                return '/dashboard/'
        except Profile.DoesNotExist:
            pass
        return '/tenant-portal/'

# --- TENANT PORTAL ---
@login_required
def tenant_portal(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('/dashboard/')
    
    payments = Payment.objects.filter(tenant__room=profile.room).order_by('-due_date') if profile.room else None
    context = {'profile': profile, 'payments': payments}
    return render(request, 'tenants/tenant_portal.html', context)

# --- ADMIN CRUD VIEWS ---
@login_required
def tenant_list(request):
    tenants = Tenant.objects.select_related('room').all()
    q = request.GET.get('q')
    room_id = request.GET.get('room')
    if q:
        tenants = tenants.filter(name__icontains=q)
    if room_id:
        tenants = tenants.filter(room_id=room_id)
    rooms = Room.objects.all()
    
    # PAGINATE: Show 5 tenants per page
    paginator = Paginator(tenants, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tenants': tenants, 
        'rooms': rooms, 
        'q': q or '', 
        'selected_room': room_id or '',
        'page_obj': page_obj,
    }
    return render(request, 'tenants/tenant_list.html', context)

def add_tenant(request):
    form = TenantForm(request.POST or None)
    if form.is_valid():
        tenant = form.save()
        update_room_occupancy(tenant.room)
        return redirect('tenant_list')
    return render(request, 'tenants/tenant_form.html', {'form': form})

def edit_tenant(request, id):
    tenant = Tenant.objects.get(id=id)
    old_room = tenant.room
    form = TenantForm(request.POST or None, instance=tenant)
    if form.is_valid():
        tenant = form.save()
        update_room_occupancy(old_room)
        update_room_occupancy(tenant.room)
        return redirect('tenant_list')
    return render(request, 'tenants/tenant_form.html', {'form': form})

@login_required
def delete_tenant(request, id):
    tenant = Tenant.objects.get(id=id)
    room = tenant.room
    tenant.delete()
    update_room_occupancy(room)
    return redirect('tenant_list')

@login_required
def submit_maintenance(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.tenant = profile.room.tenant_set.first()
            ticket.room = profile.room
            ticket.save()
            messages.success(request, "Maintenance request submitted successfully!")
            return redirect('tenant_portal')
    else:
        form = MaintenanceForm()
    return render(request, 'tenants/maintenance_form.html', {'form': form, 'profile': profile})