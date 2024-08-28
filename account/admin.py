from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from account.models import CustomUser
from account.forms import CustomUserChangeForm, CustomUserCreationForm
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm,CustomUserCreationForm
    model = CustomUser
    list_display = ('username', "is_staff", "is_active",)
    list_filter = ('username', "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ('username', "password")}),
        ("Personal Info", {"fields": ("name", "email", "photo")}),

        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Important dates", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                'username', "password1", "is_staff",
                "is_active", "name", "email", "photo","confirmation_code"

            )}
        ),
    )
    search_fields = ('username', "name", "email")
    ordering = ('username',)

    change_form_template = 'admin/auth/user/user_change_form.html'

admin.site.register(CustomUser)



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name',  'created_at', 'updated_at')
    search_fields = ('username', 'full_name', )

