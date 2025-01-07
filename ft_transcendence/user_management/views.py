from django.contrib import messages
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth import views as auth_views
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as generic_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from .forms import BlockUserForm, FriendRequestForm, TranscendenceUserCreationForm, SignInAuthenticationForm, CustomPasswordChangeForm, TranscendenceUserUpdateForm
from .models import BlockedUsers, FriendRequest, Friendship, TrUser
from pong.models import Match, TournamentParticipant

class UserProfileView(LoginRequiredMixin, generic_views.TemplateView):
    template_name = "user_management/profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        last_login = None
        if user.last_login:
            last_login = user.last_login.strftime("%d/%m/%Y at %H:%M")
        
        profile_picture = user.profile_picture.url if user.profile_picture else '/media/user/profile_pictures/foto-perfil-default.png'

        user_game_stats = self.get_user_statistics(request.user.id)

        context = {
            "last_login": last_login,
            "profile_picture": profile_picture,
            "user_game_stats": user_game_stats,
        }

        return render(request, self.template_name, context)

    def get_user_statistics(self, user):
        total_matches = (
            Match.objects.filter(player1=user).count()
            + Match.objects.filter(player2=user).count()
        )
        total_wins = Match.objects.filter(winner=user).count()
        total_tournaments = TournamentParticipant.objects.filter(player=user).count()
        total_tournament_wins = TournamentParticipant.objects.filter(
            player=user, is_eliminated=False
        ).count()

        return {
            "total_matches": total_matches,
            "total_wins": total_wins,
            "total_tournaments": total_tournaments,
            "total_tournament_wins": total_tournament_wins,
        }


class UserChatView(LoginRequiredMixin, generic_views.TemplateView):
    template_name = "user_management/chat.html"

    def get(self, request, *args, **kwargs):
        friends = Friendship.objects.filter(
            Q(first_user=request.user.id) | Q(second_user=request.user.id)
        )

        current_friends = {
            (entry.first_user if entry.first_user != request.user else entry.second_user).username: {
                'chat_room_id': entry.chat_room_id,
                'is_online': entry.first_user.is_online if entry.first_user != request.user else entry.second_user.is_online
            }
            for entry in friends
        }

        context = {
            "current_friends": current_friends,
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "user_management/chat.html", context)
        return super().get(request, *args, **kwargs)
    

class UserSignInView(auth_views.LoginView):
    template_name = "user_management/sign_in.html"
    redirect_authenticated_user = True
    # TODO: Change to homepage instead of password change page
    success_url = reverse_lazy("user_management:profile")
    form_class = SignInAuthenticationForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    

class UserSignUpView(generic_views.FormView):
    template_name = "user_management/sign_up.html"
    form_class = TranscendenceUserCreationForm
    # TODO: Change to homepage instead of password change page
    success_url = reverse_lazy("user_management:sign_in")

    def form_valid(self, form):
        form.save()
        return JsonResponse({'status': 'success'}, status=200)
    
    def form_invalid(self, form):
        if form.has_error('username'):
            messages.error(self.request, "The username is already taken.")

        elif form.has_error('password2'):
            messages.error(self.request, "The passwords do not match. Please try again.")

        if not any(form.has_error(field) for field in ['username', 'first_name', 'password2']):
            messages.error(self.request, "Please correct the errors.")

        return self.render_to_response(self.get_context_data(form=form))
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class UserChangePasswordView(
    auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView
):
    template_name = "user_management/change_password.html"
    form_class = auth_forms.PasswordChangeForm
    success_url = reverse_lazy("user_management:profile")
    form_class = CustomPasswordChangeForm

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = self.get_context_data()
            return render(request, "user_management/change_password.html", context)
        return super().get(request, *args, **kwargs)


class UserLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = reverse_lazy("user_management:sign_in")


class UserFriendListView(auth_mixins.LoginRequiredMixin, generic_views.View):
    template_name = "user_management/friend_list.html"

    def get(self, request, *args, **kwargs):
        # O form pra mandar um invite pra um usuário
        friend_request_form = FriendRequestForm()
        block_user_form = BlockUserForm()
        pending_friend_requests = FriendRequest.objects.filter(receiver=request.user)
        sent_friend_requests = FriendRequest.objects.filter(sender=request.user)
        user_update_form = TranscendenceUserUpdateForm(instance=request.user)
        # essas duas variáveis abaixo são pra filtrar o resultado da query
        # de entradas na tabela de amizade
        friends = Friendship.objects.filter(
            Q(first_user=request.user.id) | Q(second_user=request.user.id)
        )
        current_friends = [
            entry.first_user if entry.first_user != request.user else entry.second_user
            for entry in friends
        ]

        blocked_users = BlockedUsers.objects.filter(
            Q(blocker=request.user.id)
        )

        context = {
            "block_user_form": block_user_form,
            "friend_request_form": friend_request_form,
            "pending_friend_requests": pending_friend_requests,
            "sent_friend_requests": sent_friend_requests,
            "current_friends": current_friends,
            "blocked_users": blocked_users,
            "user_update_form": user_update_form,
        }
        return render(request, self.template_name, context)

class UserFriendsView(auth_mixins.LoginRequiredMixin, generic_views.View):
    template_name = "user_management/friends.html"

    def get(self, request, *args, **kwargs):
        friend_request_form = FriendRequestForm()
        block_user_form = BlockUserForm()
        all_users = TrUser.objects.all().exclude(id=request.user.id)
        received_friend_requests = FriendRequest.objects.filter(receiver=request.user)
        sent_friend_requests = FriendRequest.objects.filter(sender=request.user)
        pending_friend_requests = FriendRequest.objects.filter(
            Q(receiver=request.user) | Q(sender=request.user)
        )
        
        friends = Friendship.objects.filter(
            Q(first_user=request.user.id) | Q(second_user=request.user.id)
        )

        current_friends = {
            (entry.first_user if entry.first_user != request.user else entry.second_user).username: entry.chat_room_id
            for entry in friends
        }

        context = {
            "all_users": all_users,
            "block_user_form": block_user_form,
            "friend_request_form": friend_request_form,
            "received_friend_requests": received_friend_requests,
            "sent_friend_requests": sent_friend_requests,
            "pending_friend_requests": pending_friend_requests,
            "current_friends": current_friends,
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "user_management/friends.html", context)
        return render(request, self.template_name, context)

class UserDetailView(auth_mixins.LoginRequiredMixin, generic_views.View):
    template_name = "user_management/user_detail.html"
    
    def get_user_statistics(self, user):
        total_matches = (
            Match.objects.filter(player1=user).count()
            + Match.objects.filter(player2=user).count()
        )
        total_wins = Match.objects.filter(winner=user).count()
        total_tournaments = TournamentParticipant.objects.filter(player=user).count()
        total_tournament_wins = TournamentParticipant.objects.filter(
            player=user, is_eliminated=False
        ).count()

        return {
            "total_matches": total_matches,
            "total_wins": total_wins,
            "total_tournaments": total_tournaments,
            "total_tournament_wins": total_tournament_wins,
        }

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        
        if not user_id:
            raise Http404("User ID not provided")
        
        user = TrUser.objects.filter(id=user_id).values(
            'id', 'username', 'first_name', 'last_login', 'profile_picture'
        ).first()
        
        if not user:
            raise Http404("User not found")

        last_login = None
        if user['last_login']:
            last_login = user['last_login'].strftime("%d/%m/%Y at %H:%M")

        is_blocked = BlockedUsers.objects.filter(
            blocker=request.user.id, blocked=user_id
        ).exists()

        is_friend = Friendship.objects.filter(
            Q(first_user=request.user.id, second_user=user_id) |
            Q(first_user=user_id, second_user=request.user.id)
        ).exists()

        friendship_status = None

        if not is_friend:
            friend_request = FriendRequest.objects.filter(
                Q(sender_id=request.user.id, receiver_id=user_id) |
                Q(sender_id=user_id, receiver_id=request.user.id)
            ).first()

            if friend_request:
                friendship_status = (
                    "sent" if friend_request.sender_id == request.user.id else "received"
                )
                
        user_game_stats = self.get_user_statistics(user['id'])

        profile_picture = settings.MEDIA_URL + user['profile_picture'] if user['profile_picture'] else settings.MEDIA_URL + 'user/profile_pictures/foto-perfil-default.png'

        context = {
            "user_id": user['id'],
            "username": user['username'],
            "first_name": user['first_name'],
            "last_login": last_login,
            "is_blocked": is_blocked,
            "is_friend": is_friend,
            "friend_request": friendship_status,
            "profile_picture": profile_picture,
            "user_game_stats": user_game_stats,
        }

        return render(request, self.template_name, context)


class UserUpdateInfoView(auth_mixins.LoginRequiredMixin, generic_views.View):
    template_name = "user_management/update_info.html"

    def get(self, request, *args, **kwargs):
        user_update_form = TranscendenceUserUpdateForm(instance=request.user)

        context = {
            "user_update_form": user_update_form,
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "user_management/update_info.html", context)
        return render(request, self.template_name, context)
