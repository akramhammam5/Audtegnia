from django.contrib.auth.forms import UserChangeForm

class EditUsernameForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ('username',)