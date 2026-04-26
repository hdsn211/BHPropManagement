from django import forms
from django.contrib.auth.models import User
from .models import Tenant

class TenantForm(forms.ModelForm):
    # --- NEW FIELDS FOR ACCOUNT CREATION ---
    username = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep existing'})
    )
    password1 = forms.CharField(
        label='Password', 
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep existing'})
    )
    password2 = forms.CharField(
        label='Confirm Password', 
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Tenant
        fields = ['name', 'contact', 'email', 'start_date', 'room'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        from properties.models import Room
        self.fields['room'] = forms.ModelChoiceField(
            queryset=Room.objects.all(),
            widget=forms.Select(attrs={'class': 'form-select'}),
            required=False
        )

    # --- VALIDATION LOGIC ---
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    # --- UPDATED SAVE LOGIC ---
    def save(self, commit=True):
        tenant = super().save(commit=False)
        
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password1')

        # If a username was provided, create or update the User account
        if username:
            if tenant.user:
                tenant.user.username = username
                if password:
                    tenant.user.set_password(password)
                tenant.user.save()
            else:
                user = User.objects.create_user(username=username, password=password)
                tenant.user = user
                
        if commit:
            tenant.save()
            if tenant.user and hasattr(tenant.user, 'profile'):
                tenant.user.profile.room = tenant.room
                tenant.user.profile.save()
                
        return tenant