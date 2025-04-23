from django import forms
from .models import AdminProfile

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['full_name','phone_number','license_number','address','bio','profile_image']

        wedgets = {
            'full_name':forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control'}),
            'license_number': forms.TextInput(attrs={'class':'form-control'}),
            'bio': forms.Textarea(attrs={'class':'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }