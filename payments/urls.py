from django.urls import path
from . import views

urlpatterns = [
    # Public URL
    path('inquire/', views.submit_inquiry, name='submit_inquiry'),
    
    # Admin Payment & Inquiry URLs
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.add_payment, name='add_payment'),
    path('payments/edit/<int:id>/', views.edit_payment, name='edit_payment'),
    path('payments/delete/<int:id>/', views.delete_payment, name='delete_payment'),
    path('inquiries/', views.inquiry_list, name='inquiry_list'),
    path('generate-dues/', views.generate_dues, name='generate_dues'),
    path('maintenance/', views.MaintenanceListView.as_view(), name='maintenance_list'),
    path('maintenance/update/<int:id>/', views.update_maintenance_status, name='update_maintenance_status'),
    path('inquiry/<int:id>/read/', views.mark_inquiry_read, name='mark_inquiry_read'),
]