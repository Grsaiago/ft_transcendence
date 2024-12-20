from django.contrib import admin
from .models import TrUser, FriendRequest, Friendship, BlockedUsers

admin.site.register(TrUser)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(BlockedUsers)

# Register your models here.
