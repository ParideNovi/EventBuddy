#per includere il nostro CustomUser form per la registrazione con tale view

from django_registration.forms import RegistrationForm
from users.models import CustomUser

class CustomUserForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = CustomUser