from django import forms

from .models import CustomerProfile

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['full_name', 'phone_number', 'address', 'image', 'date_of_birth']
        widgets = {
        'full_name': forms.TextInput(attrs={'class': 'form-control'}),
        'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        'address': forms.Textarea(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

