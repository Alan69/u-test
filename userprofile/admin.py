from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'is_staff', 'is_superuser', 'is_active')

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = ('username', 'first_name', 'last_name', 'class_name')

# admin.site.unregister(User)
admin.site.register(User, UserAdmin)