from django import forms
from .models import ManagerProfile, RicePost

class ManagerProfileForm(forms.ModelForm):
    class Meta:
        model = ManagerProfile
        fields = ['full_name','phone_number','address','mill_name','mill_location','experience_year','bio','profile_image']
        widgets ={
            'full_name':forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control'}),
            'mill_name': forms.TextInput(attrs={'class':'form-control'}),
            'mill_location': forms.Textarea(attrs={'class':'form-control'}),
            'experience_year': forms.IntegerField(attrs={'class':'form-control'}),
            'bio': forms.Textarea(attrs={'class':'form-control'}),
            'profile_image': forms.ImageField(attrs={'class':'form-control'}),
        }
        