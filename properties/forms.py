from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'rent_amount', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'rent_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from properties.models import Property
        self.fields['property'] = forms.ModelChoiceField(
            queryset=Property.objects.all(),
            widget=forms.Select(attrs={'class': 'form-select'}),
            required=False
        )