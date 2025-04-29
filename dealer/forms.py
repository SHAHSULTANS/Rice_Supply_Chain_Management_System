from django import forms
from .models import DealerProfile, PaddyStock

class DealerProfileForm(forms.ModelForm):
     class Meta:
        model = DealerProfile
        exclude = ['user'] 



class PaddyStockForm(forms.ModelForm):
    class Meta:
        model = PaddyStock
        exclude = ['dealer', 'stored_since']  # Dealer set in view
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'moisture_content': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_mon': forms.NumberInput(attrs={'class': 'form-control'}),            
            'quality_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }