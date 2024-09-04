from django.urls import reverse_lazy
from django.views import generic as generic_views
from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins, views as auth_views, forms as auth_forms
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

class UserFriendListView(auth_mixins.LoginRequiredMixin, generic_views.CreateView):
    template_name = "user_management/friend_list.html"
    form_class = FriendRequestForm 
    success_url = reverse_lazy("user_management:friend_list")

    # Adiciona o campo 'sender' ao form como sendo o próprio usuário
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.sender = self.request.user
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Friend request sent successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"error: {error}")
        return super().form_invalid(form)
