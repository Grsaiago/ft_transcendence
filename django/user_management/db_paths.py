from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from .forms import FriendRequestForm

@require_POST
@login_required
def send_friend_request(request):
    form = FriendRequestForm(request.POST.copy())
    form.instance.sender = request.user
    print(form.data.appendlist)
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
def accept_friend_request(request):
    # A ação é aceitar um pedido de amizade 
    accept_form = AcceptFriendRequestForm(request.POST)
    if accept_form.is_valid():
        request_id = accept_form.cleaned_data['request_id']
        friendship_request = get_object_or_404(FriendshipRequest, id=request_id, receiver=request.user)
        # TODO: Lógica de aceitar o pedido de amizade
        messages.success(request, 'Friend request accepted successfully!')
    else:
        for _, errors in accept_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect('user_management:friend_management')
