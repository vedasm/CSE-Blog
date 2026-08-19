from django import forms
from apps.core.forms import validate_image
from .models import Event, ScheduleItem


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. National Level Hackathon 2026'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CSE Seminar Hall 3 / Online'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Event details, themes, eligibility, agenda...'}),
            'registration_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            validate_image(image)
        return image


class ScheduleItemForm(forms.ModelForm):
    class Meta:
        model = ScheduleItem
        fields = [
            'title', 'category', 'start_date', 'end_date',
            'start_time', 'end_time', 'venue', 'description',
            'registration_link', 'attachment', 'is_academic_calendar', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Internal Assessment Test 1 / Hackathon'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Main Auditorium / CSE Labs'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detailed schedule, circular instructions, timing...'}),
            'registration_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
            'is_academic_calendar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', 'End date cannot be earlier than start date.')

        return cleaned_data
