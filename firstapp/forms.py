# -*- coding: UTF-8 -*-
__author__ = 'MD'
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from models import *
from django.contrib.auth.forms import AdminPasswordChangeForm, UserChangeForm, PasswordChangeForm
from django.utils.html import format_html
from firstapp import password_validators


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see this "
                                                     "user's password, but you can change the password using "
                                                     "<a href=\"password/\">this form</a>."))


class CustomUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as before, for verification."))

    class Meta:
        model = User
        fields = ("username", 'email', 'avatar', 'mobile', 'qq', 'url')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        return user


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ('borrowing_times', 'storage_time')


class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        help_text=_('Your password must contain at least 6 character. '
                    'Your password can\'t be too similar to your other personal '
                    'information.Your password can\'t be a commonly used password.Your'
                    ' password can\'t be entirely numeric.')
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput,
                                    help_text=_('Your password must contain at least 6 character. '
                                                'Your password can\'t be too similar to your other personal '
                                                'information.Your password can\'t be a commonly used password.Your'
                                                ' password can\'t be entirely numeric.'))
