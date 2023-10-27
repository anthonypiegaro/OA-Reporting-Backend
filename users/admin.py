from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.site_header = 'Optimum Athletes'                    # default: "Django Administration"
admin.site.index_title = 'Admin Center'                 # default: "Site administration"
admin.site.site_title = 'HTML title from adminsitration'

# Register your models here.
class CustomUserAdmin(UserAdmin):
    ordering = ('last_name',)
    model = CustomUser
    list_display = ("last_name", "first_name", 'is_staff', 'is_active',)
    list_filter = ("first_name", "last_name", 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', "first_name", "last_name")}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', "first_name", "last_name", 'is_staff', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
