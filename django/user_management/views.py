from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as generic_views
from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins, views as auth_views, forms as auth_forms

from .models import FriendRequest, Friendship
from .forms import FriendRequestForm, TranscendenceUserCreationForm


class UserRegisterView(generic_views.FormView):
    template_name = "user_management/register.html"
    form_class = TranscendenceUserCreationForm
    # TODO: Change to homepage instead of password change page
    success_url = reverse_lazy("user_management:change_password")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserLoginView(auth_views.LoginView):
    template_name = "user_management/login.html"
    redirect_authenticated_user = True
    # TODO: Change to homepage instead of password change page
    success_url = reverse_lazy("user_management:change_password")

    def form_invalid(self, form):
        messages.error(self.request, 'invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("user_management:login")


class UserChangePasswordView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = "user_management/change_password.html"
    form_class = auth_forms.PasswordChangeForm
    success_url = "https://google.com"  # TODO: Redirect to homepage

class UserFriendListView(auth_mixins.LoginRequiredMixin, generic_views.View):
    template_name = "user_management/friend_list.html"

    def get(self, request, *args, **kwargs):
        # O form pra mandar um invite pra um usuário
        friend_request_form = FriendRequestForm()
        pending_friend_requests = FriendRequest.objects.filter(receiver=request.user)
        sent_friend_requests = FriendRequest.objects.filter(sender=request.user)
        # essas duas variáveis abaixo são pra filtrar o resultado da query
        # de entradas na tabela de amizade
        friends = Friendship.objects.filter(
            Q(first_user=request.user.id)
            | Q(second_user=request.user.id)
        )
        current_friends = [ entry.first_user if entry.first_user != request.user else entry.second_user for entry in friends ]

        context = {
            'friend_request_form': friend_request_form,
            'pending_friend_requests': pending_friend_requests,
            'sent_friend_requests': sent_friend_requests,
            'current_friends': current_friends,
        }
        return render(request, self.template_name, context)
