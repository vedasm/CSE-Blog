from django import forms
from .models import DepartmentDocument, PlacementStat, DepartmentMilestone, DepartmentLab


def validate_image(image):
    if image and (getattr(image, 'content_type', '') not in {'image/jpeg', 'image/png', 'image/webp'} or image.size > 5 * 1024 * 1024):
        raise forms.ValidationError('Upload a JPEG, PNG, or WEBP image no larger than 5 MB.')


class DepartmentDocumentForm(forms.ModelForm):
    class Meta:
        model = DepartmentDocument
        fields = ['title', 'category', 'academic_year', 'description', 'pdf_file', 'external_url', 'display_order', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Publications of Journals 2023-2024'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2023-2024'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief summary of the document or report contents...'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'external_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://srmvalliammai.edu.in/uploads/...pdf'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PlacementStatForm(forms.ModelForm):
    class Meta:
        model = PlacementStat
        fields = ['year', 'students_placed', 'total_offers', 'highest_package', 'average_package', 'top_recruiters', 'display_order', 'is_published']
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2024'}),
            'students_placed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '150'}),
            'total_offers': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '170'}),
            'highest_package': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12 LPA'}),
            'average_package': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '4.5 LPA'}),
            'top_recruiters': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'TCS, CTS, Wipro, Infosys, Zoho, Accenture...'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DepartmentMilestoneForm(forms.ModelForm):
    class Meta:
        model = DepartmentMilestone
        fields = ['title', 'metric_value', 'icon', 'description', 'display_order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Placements in 2023'}),
            'metric_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 149+'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fa-solid fa-briefcase'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campus placement offers secured across leading MNCs'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DepartmentLabForm(forms.ModelForm):
    class Meta:
        model = DepartmentLab
        fields = ['name', 'domain', 'computers_count', 'printers_count', 'ups_info', 'software_installed', 'image_url', 'display_order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AI & Machine Learning Lab'}),
            'domain': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Artificial Intelligence & Deep Learning'}),
            'computers_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'printers_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'ups_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10 KVA'}),
            'software_installed': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
