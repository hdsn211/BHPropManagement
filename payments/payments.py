from django import forms
from .models import Payment, Inquiry

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'due_date', 'paid_date', 'status']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'paid_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from tenants.models import Tenant
        self.fields['tenant'] = forms.ModelChoiceField(
            queryset=Tenant.objects.all(),
            widget=forms.Select(attrs={'class': 'form-select'}),
            required=True
        )


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'contact_number', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 09123456789'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'I am interested in this room...'}),
        }