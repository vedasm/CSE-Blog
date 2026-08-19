from django.contrib import admin
from .models import Faculty
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display=('name','designation','email','is_active','display_order'); list_filter=('designation','is_active'); search_fields=('name','specialization')
