from django import forms
from .models import ManagerProfile, RicePost, Purchase_paddy, PurchaseRice,PaymentForPaddy,PaymentForRice

class ManagerProfileForm(forms.ModelForm):
    class Meta:
        model = ManagerProfile
        fields = ['full_name','phone_number','transaction_password','address','mill_name','mill_location','experience_year','bio','profile_image']
        widgets ={
            'full_name':forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'transaction_password': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control'}),
            'mill_name': forms.TextInput(attrs={'class':'form-control'}),
            'mill_location': forms.Textarea(attrs={'class':'form-control'}),
            'experience_year': forms.NumberInput(attrs={'class':'form-control'}),
            'bio': forms.Textarea(attrs={'class':'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

class RicePostForm(forms.ModelForm):
    class Meta:
        model = RicePost
        fields = ['rice_name','quality', 'quantity_kg', 'price_per_kg', 'description', 'rice_image']
        widgets = {
            'rice_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quality': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_kg': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_kg': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rice_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
class Purchase_paddyForm(forms.ModelForm):
    class Meta:
        model = Purchase_paddy
        fields = ['quantity_purchased','transport_cost']
    
class PurchaseRiceForm(forms.ModelForm):
    class Meta:
        model = PurchaseRice
        fields = ['quantity_purchased','delivery_cost']
        
        
        
class PaymentForPaddyForm(forms.ModelForm):
    class Meta:
        model = PaymentForPaddy
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class PaymentForRiceForm(forms.ModelForm):
    class Meta:
        model = PaymentForRice
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }