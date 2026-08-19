from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminUser, LoginAttempt
@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    model = AdminUser
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    ordering = ('email',)
    fieldsets = ((None, {'fields': ('email', 'password')}), ('Profile', {'fields': ('first_name','last_name','role','profile_picture')}), ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}), ('Important dates', {'fields': ('last_login','date_joined')}))
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email','password1','password2','role')}),)
admin.site.register(LoginAttempt)
