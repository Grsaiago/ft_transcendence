from django.contrib.auth.forms import UserCreationForm, ValidationError
from django.db.models import Q
import django.forms as forms 
from .models import BlockedUsers, FriendRequest, Friendship, TrUser


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

class CancelFriendRequestForm(forms.Form):
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
        if not friend_request.exists():
            raise ValidationError("Friend request doesn't exist")
        return data

    # Igual ao do refuse
    def save(self, commit=True):
        friend_request = FriendRequest.objects.filter(
            sender=self.cleaned_data.get("sender"),
            receiver=self.cleaned_data.get("receiver")
        )
        if not friend_request.exists():
            raise ValidationError("Could not save the cancel of the request")
        if commit:
            friend_request.delete()
        return friend_request 


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
        if not friend_request.exists():
            raise ValidationError("Friend request doesn't exist")
        return data

    def save(self, commit=True):
        friendship = None
        friend_request = FriendRequest.objects.filter(
            sender=self.cleaned_data.get("sender"),
            receiver=self.cleaned_data.get("receiver")
        )
        if not friend_request.exists():
            raise ValidationError("Could not save the accept of the friend request")
        if commit:
            friendship = Friendship(first_user=self.cleaned_data.get("sender"),
                                    second_user=self.cleaned_data.get("receiver"))
            friendship.save()
            friend_request.delete()
        return friendship 


class RefuseFriendRequestForm(forms.Form):
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
        if not friend_request.exists():
            raise ValidationError("Friend request doesn't exist")
        return data

    def save(self, commit=True):
        friend_request = FriendRequest.objects.filter(
            sender=self.cleaned_data.get("sender"),
            receiver=self.cleaned_data.get("receiver")
        )
        if not friend_request.exists():
            raise ValidationError("Could not save the refuse of the friend request")
        if commit:
            friend_request.delete()
        return friend_request

class RemoveFriendshipForm(forms.Form):
    user_field = Friendship._meta.get_field('first_user')

    first_user = forms.ModelChoiceField(
        queryset = TrUser.objects.all(),
        required = not user_field.blank,
        help_text = user_field.help_text,
    )
    # o receiver do pedido de amizade é sempre o próprio usuário logado
    second_user = forms.ModelChoiceField(
        queryset = TrUser.objects.all(),
        required = not user_field.blank,
        help_text = user_field.help_text,
    )

    def clean(self):
        data = super().clean()
        friendship = Friendship.objects.filter(
            Q(first_user=self.cleaned_data.get('first_user'), second_user=self.cleaned_data.get('second_user'))
            | Q(first_user=self.cleaned_data.get('second_user'), second_user=self.cleaned_data.get('first_user'))
        )
        if not friendship.exists():
            raise ValidationError("Friendship doesn't exist")
        return data

    def save(self, commit=True):
        friendship = Friendship.objects.filter(
            Q(first_user=self.cleaned_data.get('first_user'), second_user=self.cleaned_data.get('second_user'))
            | Q(first_user=self.cleaned_data.get('second_user'), second_user=self.cleaned_data.get('first_user'))
        )
        if not friendship.exists():
            raise ValidationError("Could not save the removal of the friendship")
        if commit:
            friendship.delete()
        return friendship 

class BlockUserForm(forms.ModelForm):
    class Meta:
        model = BlockedUsers 
        fields = [ "blocker", "blocked" ]

    def save(self, commit=True):
        # TODO: Apagar as entradas das tabelas de Friendship e FriendRequest caso existam

        # Deletar as amizades entre esses usuários, caso existam
        Friendship.objects.filter(
            Q(first_user=self.cleaned_data.get("blocker"),
              second_user=self.cleaned_data.get("blocked"))
            | Q(first_user=self.cleaned_data.get("blocked"),
                second_user=self.cleaned_data.get("blocker"))
        ).delete()
        FriendRequest.objects.filter(
            Q(sender=self.cleaned_data.get("blocker"),
              receiver=self.cleaned_data.get("blocked"))
            | Q(sender=self.cleaned_data.get("blocked"),
                receiver=self.cleaned_data.get("blocker"))
        ).delete()
        return super().save(commit)
