from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model

# on pourra créer nos propres formulaire de création 
#ou de mofidification

class UserCreationForm(auth_forms.UserCreationForm):
    """Formulaire utiliser pour la creation de nouveau
    utilisateurs"""

    class Meta(auth_forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'email', 'password1', 'password2', 'role')


class UserChangeForm(auth_forms.UserChangeForm):
    """Formulaire pour mettre à jour les données de l'utilisateur"""

    class Meta(auth_forms.UserChangeForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'role')

