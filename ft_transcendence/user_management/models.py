import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, BooleanField

# docuemntação dos parametros para os fields das models:
# https://docs.djangoproject.com/en/5.1/ref/models/fields/#field-options


class TrUser(AbstractUser):
    # ..todos os campos de AbstractBaseUser
    profile_picture = models.ImageField(
        upload_to='user/profile_pictures',
        default='user/profile_pictures/foto-perfil-default.png',
        help_text="Foto de perfil do usuário",
        null=True,
        blank=True
    )
    is_online = models.BooleanField(
        default=False
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

    # Pra facilitar a vida dos LSPs
    objects = models.Manager()

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

    # Pra facilitar a vida dos LSPs
    objects = models.Manager()


class BlockedUsers(models.Model):
    blocker = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="blocker"
    )
    blocked = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="blocked"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Pra facilitar a vida dos LSPs
    objects = models.Manager()
