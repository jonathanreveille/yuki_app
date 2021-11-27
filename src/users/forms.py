from django.contrib.auth import forms as auth_forms, get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field


class UserCreationForm(auth_forms.UserCreationForm):
    """Form used to create a new user"""

    class Meta(auth_forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',
                  'email',
                  'first_name',
                  'email',
                  'password1',
                  'password2',
                  'role')


class UserChangeForm(auth_forms.UserChangeForm):
    """Form used to update a user's object"""

    class Meta(auth_forms.UserChangeForm.Meta):
        model = get_user_model()
        fields = ('username',
                  'email',
                  'first_name',
                  'role',
                  'host_capacity',
                  'location',
                  'avatar',
                  'postal_code',
                  'friends')
