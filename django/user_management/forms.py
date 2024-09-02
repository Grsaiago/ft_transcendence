from django.contrib.auth.forms import UserCreationForm, get_user_model
from .models import TrUser


class TranscendenceUserCreationForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = get_user_model() 
        # colocar os custom fields dentro desse parentesis
        fields = UserCreationForm.Meta.fields + ('first_name',)

    #     first_name = forms.CharField(
    #         required=False,
    #         label="user's first name",
    #         initial="Your First Name",
    #         max_length=25,
    #     )
    #     last_name = forms.CharField(
    #         required=False,
    #         label="user's last name",
    #         initial="Your last Name",
    #         max_length=25,
    #     )
    # add profile picture later
    #  profile_picture = forms.FileField(
    #      required=False,
    #      label="user's profile picture",
    #  )
