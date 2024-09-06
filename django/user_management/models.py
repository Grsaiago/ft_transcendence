import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

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

class FriendRequest(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="receiver")

    # Custom validations
    def clean(self):
        # A pessoa tentou se adicionar (haja autoestima em)
        if self.sender == self.receiver:
            raise ValidationError("Cannot send an invite to yourself")
        # Já há um pedido pendente
        if FriendRequest.objects.filter(
            sender=self.sender, receiver=self.receiver
        ).exists(): 
            raise ValidationError("Invite already sent")
        # TODO: Substituir por lógica de adicionar quando duas pessoas se mandam
        # invite
        if FriendRequest.objects.filter(
            sender=self.receiver, receiver=self.sender
        ).exists(): 
            raise ValidationError("There's already a pending request for this user")
        # Já tem amizade com essa pessoa
        if Friendship.objects.filter(
            models.Q(first_user=self.sender, second_user=self.receiver)
            | models.Q(first_user=self.receiver, second_user=self.sender)
        ).exists():
            raise ValidationError("You're already friends with this person")
        # O usuário sendo adicionado existe?
        if not TrUser.objects.get(username=self.receiver):
            raise ValidationError("The user you tried to add doesn't exist")
        return

class Friendship(models.Model):
    first_user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name="first_user")
    second_user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name="second_user")
    chat_room_id = models.UUIDField(
        null=True,
        blank=False,
        unique=True,
        default=uuid.uuid4
    )

# Create your models here.
