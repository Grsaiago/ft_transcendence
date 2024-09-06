from django.contrib.auth.forms import UserCreationForm, ValidationError
import django.forms as forms 
from .models import FriendRequest, Friendship, TrUser


class TranscendenceUserCreationForm(UserCreationForm):
    usable_password = None

    class Meta(UserCreationForm.Meta):
        model = TrUser 
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

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = [ "sender", "receiver" ]


class AcceptFriendRequestForm(forms.Form):
    # Essa api do _meta está pra ser estabilizada
    sender_field = FriendRequest._meta.get_field('sender')
    receiver_field = FriendRequest._meta.get_field('receiver')

    sender = forms.ModelChoiceField(
        queryset = TrUser.objects.all(),
        required = not sender_field.blank,
        help_text = sender_field.help_text,
    )

    # o receiver do pedido de amizade é sempre o próprio usuário logado
    receiver = forms.ModelChoiceField(
        queryset = TrUser.objects.all(),
        required = not sender_field.blank,
        help_text = sender_field.help_text,
    )

    def clean(self):
        data = super().clean()
        friend_request = FriendRequest.objects.filter(
            sender=self.cleaned_data.get("sender"),
            receiver=self.cleaned_data.get("receiver")
        )
        if friend_request is None:
            raise ValidationError("Friend request doesn't exist")
        return data

    def save(self, commit=True):
        print("Entrou no save do AcceptFriendRequestForm")
        friendship = None
        friend_request = FriendRequest.objects.get(
            sender=self.cleaned_data.get("sender"),
            receiver=self.cleaned_data.get("receiver")
        )
        if commit:
            friendship = Friendship(first_user=self.cleaned_data.get("sender"),
                                    second_user=self.cleaned_data.get("receiver"))
            friendship.save()
            friend_request.delete()
        return friendship 
