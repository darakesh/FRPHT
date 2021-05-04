from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit , Layout, Row, Column, Button, Field, HTML


User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'userID','username','father_name','age','gender','blood_group','number','emergency_number','userphoto', 'is_doctor']

    def clean_password_2(self):
        password = self.cleaned_data.get("password")
        password_2 = self.cleaned_data.get("password_2")
        if password and password_2 and password != password_2:
            self.add_error("password_2", "Passwords don't match")
        return password_2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)
        self.helper = FormHelper()
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class ='form-group col-md-4 mb-0'),
                Column('userID', css_class ='form-group col-md-3 mb-0'),
                Column('username', css_class ='form-group col-md-5 mb-0'),
                css_class= 'form-row'
            ),
            Row(
                Column('password', css_class = 'form-group col-md-6 mb-0'),
                Column('password_2', css_class = 'form-group col-md-6 mb-0'),
                css_class= 'form-row'
            ),
            Row(
                Column('father_name', css_class ='form-group col-md-6 mb-0'),
                Column('age', css_class ='form-group col-md-2 mb-0'),
                Column('gender', css_class ='form-group col-md-2 mb-0'),
                Column('blood_group', css_class ='form-group col-md-2 mb-0'),
                css_class= 'form-row'
            ),
            Row(
                Column('number', css_class = 'form-group col-md-6 mb-0'),
                Column('emergency_number', css_class = 'form-group col-md-6 mb-0'),
                css_class= 'form-row'
            ),
            Field('userphoto'),
            Field('is_doctor'),
            HTML('<input type="submit" class="btn btn-success" name="submit" value="{{btn}}"> '),
            HTML(' <a class="btn btn-secondary" href= "{% url clnk %}">Cancel</a>'),
        )



class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','father_name','age','gender','blood_group','number','emergency_number','userphoto',]

    def save(self, commit=True):
        user = super(UserEditForm, self).save()
        return user

    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)
        self.helper = FormHelper()
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Field('username'),
            Row(
                Column('father_name', css_class ='form-group col-md-6 mb-0'),
                Column('age', css_class ='form-group col-md-2 mb-0'),
                Column('gender', css_class ='form-group col-md-2 mb-0'),
                Column('blood_group', css_class ='form-group col-md-2 mb-0'),
                css_class= 'form-row'
            ),
            Row(
                Column('number', css_class = 'form-group col-md-6 mb-0'),
                Column('emergency_number', css_class = 'form-group col-md-6 mb-0'),
                css_class= 'form-row'
            ),
            Field('userphoto'),
            HTML('<input type="submit" class="btn btn-success" name="submit" value="{{btn}}"> '),
            HTML(' <a class="btn btn-secondary" href= "{% url clnk id %}">Cancel</a>'),
        )




class AccountAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email','userID','username' ,'is_doctor','userphoto']

    def clean_password_2(self):
        password = self.cleaned_data.get("password")
        password_2 = self.cleaned_data.get("password_2")
        if password and password_2 and password != password_2:
            self.add_error("password_2", "Passwords don't match")
        return password_2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AccountAdminCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AccountAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'userID','username', 'password', 'is_active', 'is_doctor','father_name','age','gender','blood_group','number','emergency_number','userphoto']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
