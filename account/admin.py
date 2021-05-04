from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from account.forms import AccountAdminCreationForm, AccountAdminChangeForm

admin.site.unregister(Group)

Account = get_user_model()

@admin.register(Account)
class AccountAdmin(UserAdmin):
    # The forms to add and change user instances
    form = AccountAdminChangeForm
    add_form = AccountAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['userID', 'username', 'email', 'is_doctor', 'is_active']
    list_filter = ['is_doctor','is_active']
    readonly_fields = ('date_joined','last_login','is_superuser')
    fieldsets = (
        (None, {'fields': ('email','userID', 'password')}),
        ('Personal info', {'fields': ('username','father_name','age','gender','blood_group','number','emergency_number','userphoto','date_joined','last_login')}),
        ('Permissions', {'fields': ('is_doctor','is_active', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','userID', 'password', 'password_2', 'userphoto' , 'is_doctor')}
        ),
    )
    search_fields = ['email','userID','username']
    ordering = ['userID']
    filter_horizontal = ()
