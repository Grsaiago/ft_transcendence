import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

# docuemntação dos parametros para os fields das models:
# https://docs.djangoproject.com/en/5.1/ref/models/fields/#field-options


class TrUser(AbstractUser):
    # ..todos os campos de AbstractBaseUser
    profile_picture = models.TextField(
        verbose_name="base64 encoding of the user's pfp",
        null=True,
        blank=True,
        unique=False,
        default=None,
    )
    updated_at = models.DateTimeField(auto_now=True)


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="sender"
    )
    receiver = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="receiver"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Custom validations
    def clean(self):
        super().clean()
        # A pessoa tentou se adicionar (haja autoestima em)
        if self.sender == self.receiver:
            raise ValidationError("Cannot send an invite to yourself")
        if BlockedUsers.objects.filter(
            blocker=self.sender, blocked=self.receiver
        ).exists():
            raise ValidationError("You blocked this user already")
        if BlockedUsers.objects.filter(
            blocker=self.receiver, blocked=self.sender
        ).exists():
            raise ValidationError("This user blocked you. sorry :c")
        # Já há um pedido pendente
        if FriendRequest.objects.filter(
            sender=self.sender, receiver=self.receiver
        ).exists():
            raise ValidationError("Invite already sent")
        # quando duas pessoas se mandam invite
        if FriendRequest.objects.filter(
            sender=self.receiver, receiver=self.sender
        ).exists():
            raise ValidationError("There's already a pending request for this user")
        # Já tem amizade com essa pessoa
        if Friendship.objects.filter(
            Q(first_user=self.sender, second_user=self.receiver)
            | Q(first_user=self.receiver, second_user=self.sender)
        ).exists():
            raise ValidationError("You're already friends with this person")
        # O usuário sendo adicionado existe?
        if not TrUser.objects.get(username=self.receiver):
            raise ValidationError("The user you tried to add doesn't exist")
        return


class Friendship(models.Model):
    first_user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="first_user"
    )
    second_user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="second_user"
    )
    chat_room_id = models.UUIDField(
        null=True, blank=False, unique=True, default=uuid.uuid4
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlockedUsers(models.Model):
    blocker = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="blocker"
    )
    blocked = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="blocked"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.blocker == self.blocked:
            raise ValidationError("Cannot block yourself")
        # Usuário já foi bloqueado
        if BlockedUsers.objects.filter(
            Q(blocker=self.blocker, blocked=self.blocked)
        ).exists():
            raise ValidationError("User already blocked")
        # Usuário já te bloqueou
        if BlockedUsers.objects.filter(
            Q(blocker=self.blocked, blocked=self.blocker)
        ).exists():
            raise ValidationError("User already blocked you")
        return
