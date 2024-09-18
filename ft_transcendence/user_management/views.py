from django.contrib import messages
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth import views as auth_views
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as generic_views
from django.views.generic import TemplateView

from .forms import BlockUserForm, FriendRequestForm, TranscendenceUserCreationForm
from .models import FriendRequest, Friendship

class BaseTemplateView(TemplateView):
    template_name = "user_management/base.html"

class UserRegisterView(generic_views.FormView):
    template_name = "user_management/register.html"
    form_class = TranscendenceUserCreationForm
    # TODO: Change to homepage instead of password change page
    success_url = reverse_lazy("user_management:friend_list")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = self.get_context_data()
            return render(request, "user_management/register_block.html", context)
        return super().get(request, *args, **kwargs)


class UserLoginView(auth_views.LoginView):
    template_name = "user_management/login.html"
    redirect_authenticated_user = True
    # TODO: Change to homepage instead of password change page
    success_url = reverse_lazy("user_management:friend_list")

    def form_invalid(self, form):
        messages.error(self.request, "invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))
    
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Retorna apenas o bloco de conteúdo
            return render(request, "user_management/login_block.html", self.get_context_data())
        # Renderiza o layout completo se não for AJAX
        return super().get(request, *args, **kwargs)


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("user_management:login")


class UserChangePasswordView(
    auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView
):
    template_name = "user_management/change_password.html"
    form_class = auth_forms.PasswordChangeForm
    success_url = reverse_lazy("user_management:friend_list")

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Retorna apenas o bloco de conteúdo
            return render(request, "user_management/change_password_block.html", self.get_context_data())
        # Renderiza o layout completo se não for AJAX
        return super().get(request, *args, **kwargs)


class UserFriendListView(auth_mixins.LoginRequiredMixin, generic_views.View):
    template_name = "user_management/friend_list.html"

    def get(self, request, *args, **kwargs):
        # O form pra mandar um invite pra um usuário
        friend_request_form = FriendRequestForm()
        block_user_form = BlockUserForm()
        pending_friend_requests = FriendRequest.objects.filter(receiver=request.user)
        sent_friend_requests = FriendRequest.objects.filter(sender=request.user)
        # essas duas variáveis abaixo são pra filtrar o resultado da query
        # de entradas na tabela de amizade
        friends = Friendship.objects.filter(
            Q(first_user=request.user.id) | Q(second_user=request.user.id)
        )
        current_friends = [
            entry.first_user if entry.first_user != request.user else entry.second_user
            for entry in friends
        ]

        context = {
            "block_user_form": block_user_form,
            "friend_request_form": friend_request_form,
            "pending_friend_requests": pending_friend_requests,
            "sent_friend_requests": sent_friend_requests,
            "current_friends": current_friends,
        }

        # Verifica se é uma requisição AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "user_management/friend_list_block.html", context)
        
        return render(request, self.template_name, context)
