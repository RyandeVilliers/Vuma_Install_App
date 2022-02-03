from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# translates strings into readable form
from django.utils.translation import gettext as _


from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Section
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
            }),
    )
# start
# class StatusAdminInline(admin.TabularInline):
#     model = models.Status

# class InstallAdmin(admin.ModelAdmin):
#     inlines = (StatusAdminInline,)
# end

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Status)
admin.site.register(models.Installation)
#
# admin.site.register(models.Installation, InstallAdmin)

