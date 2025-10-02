from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('University Info', {
            'fields': ('user_type', 'employee_id', 'phone_number', 'profile_picture',
                      'date_of_birth', 'address', 'emergency_contact')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('University Info', {
            'fields': ('user_type', 'employee_id', 'phone_number', 'date_of_birth')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User Profile Admin"""
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)
