from logging import log
from django import http
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from .models import Friendship, TrUser, BlockedUsers, FriendRequest


from .forms import (
    AcceptFriendRequestForm,
    BlockUserForm,
    CancelFriendRequestForm,
    FriendRequestForm,
    RefuseFriendRequestForm,
    RemoveFriendshipForm,
    TranscendenceUserUpdateForm,
    UnblockUserForm,
    CustomPasswordChangeForm,
    SignInAuthenticationForm,
    TranscendenceUserCreationForm,
)

MAX_USER_PFP_SIZE = 1 * 1024 * 1024

# TODO: Esses redirects estão sendo evitados no front, eles só estão aqui
# pra podermos testar as rotas na página friend_list.

@require_POST
@login_required
def send_friend_request(request: HttpRequest):
    post_data = request.POST.copy()
    post_data["sender"] = request.user
    form = FriendRequestForm(post_data)
    if form.is_valid():
        form.save()
    else:
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error: {error}")
    return HttpResponse("Created successfully")


@require_POST
@login_required
def cancel_friend_request(request: HttpRequest):
    # A ação é aceitar um pedido de amizade
    post_data = request.POST.copy()
    post_data["sender"] = request.user
    cancel_form = CancelFriendRequestForm(post_data)
    if cancel_form.is_valid():
        # Lógica de recusar o pedido de amizade tá dentro do form
        cancel_form.save()
    else:
        for _, errors in cancel_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect("user_management:friend_list")


@require_POST
@login_required
def accept_friend_request(request: HttpRequest):
    # A ação é aceitar um pedido de amizade
    post_data = request.POST.copy()
    post_data["receiver"] = request.user
    accept_form = AcceptFriendRequestForm(post_data)
    if accept_form.is_valid():
        # Lógica de aceitar o pedido de amizade tá dentro do form
        accept_form.save()
    else:
        for _, errors in accept_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect("user_management:friend_list")


@require_POST
@login_required
def refuse_friend_request(request: HttpRequest):
    # A ação é aceitar um pedido de amizade
    post_data = request.POST.copy()
    post_data["receiver"] = request.user
    refuse_form = RefuseFriendRequestForm(post_data)
    if refuse_form.is_valid():
        # Lógica de recusar o pedido de amizade tá dentro do form
        refuse_form.save()
    else:
        for _, errors in refuse_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect("user_management:friend_list")


@require_POST
@login_required
def remove_friendship(request: HttpRequest):
    # A ação é aceitar um pedido de amizade
    post_data = request.POST.copy()
    post_data["second_user"] = request.user
    remove_friendship_form = RemoveFriendshipForm(post_data)
    if remove_friendship_form.is_valid():
        # Lógica de recusar o pedido de amizade tá dentro do form
        remove_friendship_form.save()
    else:
        for _, errors in remove_friendship_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect("user_management:friend_list")


@require_POST
@login_required
def block_user(request: HttpRequest):
    # A ação é bloquear um usuário
    post_data = request.POST.copy()
    post_data["blocker"] = request.user
    block_user_form = BlockUserForm(post_data)
    if block_user_form.is_valid():
        # Lógica de bloquear o usuário tá na model e o form chama
        block_user_form.save()
    else:
        for _, errors in block_user_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect("user_management:friend_list")

@require_POST
@login_required
def unblock_user(request: HttpRequest):
    post_data = request.POST.copy()
    post_data["blocker"] = request.user

    unblock_user_form = UnblockUserForm(post_data)
    if unblock_user_form.is_valid():
        unblock_user_form.save()
    else:
        for _, errors in unblock_user_form.errors.items():
            for error in errors:
                messages.error(request, f"error: {error}")
    return redirect("user_management:friend_list")

@require_GET
@login_required
def get_user_friends(request: HttpRequest):    
    friends = Friendship.objects.filter(
        Q(first_user=request.user.id) | Q(second_user=request.user.id)
    )
    
    friends_list = []
    for entry in friends:
        # Determina quem é o amigo (não o usuário atual)
        friend = entry.first_user if entry.first_user != request.user else entry.second_user
        
        # Obtém as informações detalhadas do amigo
        friend_data = TrUser.objects.filter(id=friend.id).values(
            'id', 'username', 'first_name', 'last_login'
        ).first()

        # Adiciona ao dicionário
        if friend_data:
            friends_list.append({
                "id": friend_data['id'],
                "username": friend_data['username'],
                "first_name": friend_data['first_name'],
                "last_login": friend_data['last_login'],
            })
    
    response = JsonResponse({"friends": friends_list})
    return response


@require_GET
@login_required
def get_all_users_deprecated(request: HttpRequest):
    # Obtenha todos os usuários do sistema, excluindo o usuário atual
    all_users = TrUser.objects.exclude(id=request.user.id)
    
    users_list = []
    for user in all_users:
        # Verifica se o usuário está bloqueado
        is_blocked = BlockedUsers.objects.filter(
            blocker=request.user.id, blocked=user.id
        ).exists()
        
        # Verifica se há um pedido de amizade relacionado
        friend_request = FriendRequest.objects.filter(
            sender_id=request.user.id, receiver_id=user.id
        ).first()
        
        if not friend_request:
            friend_request = FriendRequest.objects.filter(
                sender_id=user.id, receiver_id=request.user.id
            ).first()
        
        # Determina o estado do pedido de amizade
        if friend_request:
            friendship_status = (
                "sender" if friend_request.sender_id == request.user.id else "receiver"
            )
        else:
            friendship_status = None

        # Verifica se os usuários já são amigos
        is_friend = Friendship.objects.filter(
            Q(first_user=request.user.id, second_user=user.id) |
            Q(first_user=user.id, second_user=request.user.id)
        ).exists()
        
        # Adiciona os dados do usuário à lista
        users_list.append({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_login": user.last_login,
            "is_blocked": is_blocked,
            "friend_status": is_friend,
            "friend_request_status": friendship_status,
        })
    
    response = JsonResponse({"users": users_list})
    return response


@require_GET
@login_required
def get_all_users(request: HttpRequest):
    # Obtenha todos os usuários do sistema, excluindo o usuário atual
    all_users = TrUser.objects.exclude(id=request.user.id)

    users_list = []
    for user in all_users:
        #Verifica se tem pedido de amizade pendente
        pending_friend_request = FriendRequest.objects.filter(
                Q(sender_id=request.user.id, receiver_id=user.id) |
                Q(sender_id=user.id, receiver_id=request.user.id)
        ).exists()

        # Adiciona os dados do usuário à lista
        users_list.append({
            "id": user.id,
            "username": user.username,
            "pending_friend_request": pending_friend_request,
        })

    response = JsonResponse({"users": users_list})
    return response

@require_GET
@login_required
def get_user_details(request, user_id):
    try:
        # Obtenha as informações detalhadas do usuário solicitado
        user = TrUser.objects.filter(id=user_id).values(
            'id', 'username', 'first_name', 'last_login'
        ).first()

        if not user:
            return JsonResponse({"error": "User not found."}, status=404)

        # Verifica se o usuário está bloqueado
        is_blocked = BlockedUsers.objects.filter(
            blocker=request.user.id, blocked=user_id
        ).exists()

        # Verifica se há um pedido de amizade relacionado
        friend_request = FriendRequest.objects.filter(
            sender_id=request.user.id, receiver_id=user_id
        ).first()

        if not friend_request:
            friend_request = FriendRequest.objects.filter(
                sender_id=user_id, receiver_id=request.user.id
            ).first()

        # Determina o estado do pedido de amizade
        if friend_request:
            friendship_status = (
                "sender" if friend_request.sender_id == request.user.id else "receiver"
            )
        else:
            friendship_status = None

        # Verifica se os usuários já são amigos
        is_friend = Friendship.objects.filter(
            Q(first_user=request.user.id, second_user=user_id) |
            Q(first_user=user_id, second_user=request.user.id)
        ).exists()

        # Cria a resposta com os detalhes do usuário
        user_details = {
            "id": user['id'],
            "username": user['username'],
            "first_name": user['first_name'],
            "last_login": user['last_login'],
            "is_blocked": is_blocked,
            "friend_status": is_friend,
            "friend_request_status": friendship_status,
        }

        return JsonResponse(user_details)

    except Exception as e:
        return JsonResponse({"error": "An error occurred.", "details": str(e)}, status=500)

@require_POST
@login_required
def update_user(request: HttpRequest):
    post_data = request.POST.copy()
    update_user_form =  TranscendenceUserUpdateForm(post_data, request.FILES, instance=request.user)
    # verificar o tamanho do arquivo
    if len(request.FILES.keys()) > 0:
        total_size = sum(file.size for file in request.FILES.values())
        print(total_size)
        if total_size > MAX_USER_PFP_SIZE:
            messages.error(request, "invalid body size.")
            return HttpResponse(status=400) 
    if update_user_form.is_valid():
        update_user_form.save()
        return HttpResponse(status=200)
    else:
        messages.error(request, "There was an error with your submission.")
        return HttpResponse(status=400) 

@require_POST
@login_required
def change_password(request: HttpRequest):
    # Cria uma instância do formulário de alteração de senha com os dados enviados
    form = CustomPasswordChangeForm(user=request.user, data=request.POST)
    
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, request.user)
        return HttpResponse(status=200)
    else:
        if form.has_error('old_password'):
            messages.error(request, "Invalid old password.")
        elif form.has_error('new_password2'):
            messages.error(request, "Invalid new password.")
        else:
            messages.error(request, "There was an error with your submission.")
        return HttpResponse(status=400) 

@require_POST
def sign_in(request: HttpRequest):
    form = SignInAuthenticationForm(data=request.POST)
    
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return HttpResponse(status=200)
    else:
        if form.has_error():
            messages.error(request, "Invalid username or password")
        return HttpResponse(status=400) 
    

@require_POST
def sign_up(request: HttpRequest):
    form = TranscendenceUserCreationForm(data=request.POST)
    
    if form.is_valid():
        form.save()
        return HttpResponse(status=200)
    else:
        if form.has_error('username'):
            messages.error(self.request, "The username is already taken.")

        elif form.has_error('password2'):
            messages.error(self.request, "The passwords do not match. Please try again.")

        if not any(form.has_error(field) for field in ['username', 'first_name', 'password2']):
            messages.error(self.request, "Please correct the errors.")
        return HttpResponse(status=400) 

