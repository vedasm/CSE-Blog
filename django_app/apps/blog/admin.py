from django.contrib import admin
from .models import Blog,Category
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=('title','status','category','author','published_at');list_filter=('status','category');search_fields=('title','tags');prepopulated_fields={'slug':('title',)}
admin.site.register(Category)
