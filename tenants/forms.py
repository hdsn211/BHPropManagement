from django import forms
from .models import Tenant

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'contact', 'email', 'start_date'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        from properties.models import Room
        self.fields['room'] = forms.ModelChoiceField(
            queryset=Room.objects.all(),
            widget=forms.Select(attrs={'class': 'form-select'}),
            required=False
        )