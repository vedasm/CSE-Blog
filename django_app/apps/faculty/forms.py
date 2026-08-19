from django import forms
from apps.core.forms import validate_image
from .models import Faculty


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dr. B. Vanathi'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Artificial Intelligence, Computer Vision, Big Data'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. hod.cse@srmvalliammai.ac.in'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +91 9841017713'}),
            'profile_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://srmvalliammai.irins.org/profile/177877'}),
            'scholar_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://scholar.google.com/citations?...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'id': 'facultyPhotoInput'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Faculty background, educational qualifications, research interests...'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_photo(self):
        image = self.cleaned_data.get('photo')
        if image:
            validate_image(image)
        return image
