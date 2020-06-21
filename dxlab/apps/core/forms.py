from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    ReadOnlyPasswordHashField,
)

from dxlab.apps.core.models import User


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        if hasattr(self.fields, 'username'):
            del self.fields['username']

    class Meta:
        model = User
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        if hasattr(self.fields, 'username'):
            del self.fields['username']

    class Meta:
        model = User
        fields = '__all__'
