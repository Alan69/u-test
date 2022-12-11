from django.contrib import admin
from .models import Profile, Teacher
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

class UserProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    
class UserTeacherInLine(admin.StackedInline):
    model = Teacher
    can_delete = False

class AccountsUserAdmin(AuthUserAdmin):
    def add_view(self, *args, **kwargs):
        self.inlines =[]
        return super(AccountsUserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines =[UserProfileInLine,  UserTeacherInLine]
        return super(AccountsUserAdmin, self).change_view(*args, **kwargs)

admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)