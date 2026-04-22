from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # Auth & Portal
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('tenant-portal/', views.tenant_portal, name='tenant_portal'),
    
    # Admin Tenant CRUD
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('tenants/add/', views.add_tenant, name='add_tenant'),
    path('tenants/edit/<int:id>/', views.edit_tenant, name='edit_tenant'),
    path('tenants/delete/<int:id>/', views.delete_tenant, name='delete_tenant'),

    path('tenant/maintenance/', views.submit_maintenance, name='submit_maintenance'),
]

