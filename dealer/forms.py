from django import forms
from .models import DealerProfile, PaddyPurchaseFromFarmer, PaddyStock
from django.core.exceptions import ValidationError

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
            # 'price_per_something': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_mon': forms.NumberInput(attrs={'class': 'form-control'}),  
            # corrected
            'quality_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }
        
        
        
from django import forms
from .models import DealerProfile, CustomUser

class DealerProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = DealerProfile
        fields = [
            'first_name', 'last_name', 'email',# from User
            'license_number', 'storage_capacity',
            'district', 'upazila', 'union', 'address' # from DealerProfile
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        dealer = super().save(commit=False)
        if commit:
            dealer.user.first_name = self.cleaned_data['first_name']
            dealer.user.last_name = self.cleaned_data['last_name']
            dealer.user.email = self.cleaned_data['email']
            dealer.user.save()
            dealer.save()
        return dealer
    
    
# --- Purchase Form ---
class PaddyPurchaseForm(forms.ModelForm):
    class Meta:
        model = PaddyPurchaseFromFarmer
        fields = [
            'farmer_name', 'farmer_phone', 'paddy_type', 'quantity',
            'purchase_price_per_mon', 'moisture_content',
            'transport_cost', 'other_costs',
            'notes'
        ]
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_moisture_content(self):
        moisture = self.cleaned_data['moisture_content']
        if not 5 <= moisture <= 25:
            raise ValidationError("Moisture content must be between 5% and 25%")
        return moisture
    
    
