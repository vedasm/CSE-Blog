from django import forms
from .models import NewsItem


class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = [
            'title',
            'category',
            'summary',
            'content',
            'is_pinned',
            'attachment',
            'external_link',
            'is_published',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter announcement or news headline...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-select-lg'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Short summary for home feed cards (optional - auto-extracted if empty)...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 7,
                'placeholder': 'Enter complete announcement details, instructions, deadlines, or circular text...'
            }),
            'is_pinned': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'external_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/register-or-view'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
