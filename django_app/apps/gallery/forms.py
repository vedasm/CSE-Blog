from django import forms
from apps.core.forms import validate_image
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected=True
class GalleryUploadForm(forms.Form):
    images=forms.FileField(widget=MultiFileInput(attrs={'multiple':True,'accept':'image/jpeg,image/png,image/webp'}))
    category=forms.CharField(max_length=100)
    def clean_images(self):
        images=self.files.getlist('images')
        if not images:raise forms.ValidationError('Choose at least one image.')
        for image in images:validate_image(image)
        return images
