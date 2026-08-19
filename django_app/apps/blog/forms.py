from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from apps.core.forms import validate_image
from .models import Blog


class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'author', 'category', 'featured_image', 'content', 'tags', 'status', 'published_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Building Scalable Microservices with Python & Docker'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. building-scalable-microservices'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control', 'id': 'featuredImageInput'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AI, Machine Learning, Python, Web3'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        if image:
            validate_image(image)
        return image


class StudentBlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        fields = ['title', 'category', 'featured_image', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Building Scalable Microservices with Python & Docker'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control', 'id': 'featuredImageInput'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AI, Machine Learning, Python, Web3'}),
        }

    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        if image:
            validate_image(image)
        return image
