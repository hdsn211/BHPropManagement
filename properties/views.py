from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from .models import Property, Room
from .forms import RoomForm
from tenants.models import Tenant
from payments.models import Payment
from payments.forms import InquiryForm

# --- PUBLIC VIEWS ---
def public_home(request):
    properties = Property.objects.all()
    return render(request, 'properties/public_home.html', {'properties': properties})

def public_room_list(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    rooms = Room.objects.filter(property=property, is_occupied=False)
    form = InquiryForm()
    context = {'property': property, 'rooms': rooms, 'form': form}
    return render(request, 'properties/public_room_list.html', context)

@login_required
def room_list(request):
    rooms = Room.objects.select_related('property').all().order_by('name')
    # Paginate (Show 10 rooms per page)
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'properties/room_list.html', context)

@login_required
def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    current_tenant = Tenant.objects.filter(room=room).first()
    payments = Payment.objects.filter(tenant__room=room).select_related('tenant')
    context = {'room': room, 'current_tenant': current_tenant, 'payments': payments}
    return render(request, 'properties/room_detail.html', context)

@login_required
def add_room(request):
    form = RoomForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'properties/room_form.html', {'form': form})

@login_required
def edit_room(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(request.POST or None, request.FILES or None, instance=room)
    if form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'properties/room_form.html', {'form': form})

@login_required
def delete_room(request, id):
    room = Room.objects.get(id=id)
    room.delete()
    return redirect('room_list')