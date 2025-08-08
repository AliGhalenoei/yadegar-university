from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserChangeForm , UserCreationForm
from .models import User , OTP
# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email","username","is_admin","is_superuser","id"]
    list_filter = ["is_admin" , "is_superuser"]
    search_fields = ["email","isername","id"]
    filter_horizontal = ()
    ordering = ["-id"]

    fieldsets = (
        ("اطلاعات کاربر",{"fields":("email","username","password")}),
        ("سطح دسترسی کاربر",{"fields":("is_active","is_admin","is_superuser")}),
    )

    add_fieldsets = (
        ("اطلاعات کاربری",{"fields":("email","username","password","password2")}),
    )

admin.site.unregister(Group)
admin.site.register(User,UserAdmin)


@admin.register(OTP)
class OtpAdmin(admin.ModelAdmin):
    list_display = ["email" , "code"]

