from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from .forms import CancelFriendRequestForm, FriendRequestForm, AcceptFriendRequestForm, RefuseFriendRequestForm, RemoveFriendshipForm

@require_POST
@login_required
def send_friend_request(request: HttpRequest):
    post_data = request.POST.copy()
    post_data['sender'] = request.user
    form = FriendRequestForm(post_data)
    if form.is_valid():
        form.save()
        messages.success(request, 'Friend request sent successfully!')
    else:
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error: {error}")
    return redirect('user_management:friend_list')

@require_POST
@login_required
def cancel_friend_request(request: HttpRequest):
    # A ação é aceitar um pedido de amizade 
    post_data = request.POST.copy()
    post_data['sender'] = request.user
    cancel_form = CancelFriendRequestForm(post_data)
    if cancel_form.is_valid():
        # Lógica de recusar o pedido de amizade tá dentro do form
        cancel_form.save()
        messages.success(request, 'Friend request canceled successfully!')
    else:
        for _, errors in cancel_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect('user_management:friend_list')

@require_POST
@login_required
def accept_friend_request(request: HttpRequest):
    # A ação é aceitar um pedido de amizade 
    post_data = request.POST.copy()
    post_data['receiver'] = request.user
    accept_form = AcceptFriendRequestForm(post_data)
    if accept_form.is_valid():
        # Lógica de aceitar o pedido de amizade tá dentro do form
        accept_form.save()
        messages.success(request, 'Friend request accepted successfully!')
    else:
        for _, errors in accept_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect('user_management:friend_list')

@require_POST
@login_required
def refuse_friend_request(request: HttpRequest):
    # A ação é aceitar um pedido de amizade 
    post_data = request.POST.copy()
    post_data['receiver'] = request.user
    refuse_form = RefuseFriendRequestForm(post_data)
    if refuse_form.is_valid():
        # Lógica de recusar o pedido de amizade tá dentro do form
        refuse_form.save()
        messages.success(request, 'Friend request refused successfully!')
    else:
        for _, errors in refuse_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect('user_management:friend_list')

@require_POST
@login_required
def remove_friendship(request: HttpRequest):
    # A ação é aceitar um pedido de amizade 
    post_data = request.POST.copy()
    post_data['second_user'] = request.user
    remove_friendship_form = RemoveFriendshipForm(post_data)
    if remove_friendship_form.is_valid():
        # Lógica de recusar o pedido de amizade tá dentro do form
        remove_friendship_form.save()
        messages.success(request, 'Friendship removed successfully!')
    else:
        for _, errors in remove_friendship_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect('user_management:friend_list')
