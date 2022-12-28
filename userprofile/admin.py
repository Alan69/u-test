from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from import_export import resources, fields, resources, widgets
from import_export.admin import ImportExportModelAdmin

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id','username', 'password','first_name', 'last_name')

class UserProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False

class AccountsUserAdmin(AuthUserAdmin, ImportExportModelAdmin):
    list_display = ('id','username','first_name', 'last_name')
    resource_class = UserResource
    def add_view(self, *args, **kwargs):
        self.inlines =[]
        return super(AccountsUserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines =[UserProfileInLine]
        return super(AccountsUserAdmin, self).change_view(*args, **kwargs)



#profile import
class ProfileResource(resources.ModelResource):

    user = fields.Field(
        attribute="User",
        column_name="username",
        widget=widgets.ForeignKeyWidget(User, 'username'),
    )

    class Meta:
        model = Profile
        fields = ('id', 'user__username', 'class_name', 'school', 'region')

class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource


admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)
admin.site.register(Profile, ProfileAdmin)