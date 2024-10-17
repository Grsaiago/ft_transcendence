from typing import List, TypedDict, Union
import json
from uuid import UUID
from django.db.models import Q
from django.core.cache import cache
import user_management.models as social_models
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import InMemoryChannelLayer
from channels_redis.core import RedisChannelLayer
from asgiref.sync import sync_to_async


class ChatMessage(TypedDict):
    type: str
    chat_id: str
    sender: str
    message: str

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        # essa variável vai ser usada para manter registro de quais
        # chats esse usuário tá inscrito, pra facilitar o cleanup no disconect
        self.dynamic_groups: List[str] = []
        # add some types to make development more sane
        self.channel_layer: Union[InMemoryChannelLayer, RedisChannelLayer]
        self.scope: dict


    groups: List[str] = ['general_chat']


    async def connect(self):
        user_id = self.scope['user'].id
        groups_to_add: List[UUID] = await sync_to_async(list)(social_models.Friendship.objects.filter(
            Q(first_user=self.scope['user'])
            | Q(second_user=self.scope['user'])
        ).values_list('chat_room_id', flat=True))

        for group in groups_to_add:
            await self.add_to_group(str(group))
        # criar o mapeamento user_id->channel
        cache.set(f"user_channels:{user_id}", self.channel_name)

        await self.accept()


    async def disconnect(self, code):
        user_id = self.scope['user'].id

        for group in self.dynamic_groups:
            await self.remove_from_group(group)
        # deletar o mapeamento user_id->channel
        cache.delete(f"user_channels:{user_id}")


    # aqui é quando o servidor recebe uma mensagem qualquer de um websocket
    # e aqui ele só dá um broadcast nessa mensagem pro chat target.
    # A gente vai precisar de uma chave no objeto recebido pra fazer o decode
    # e conseguir dar handle em eventos do jogo ou eventos de chat ou diferentes eventos
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(str(text_data))
        message = text_data_json["message"]
        chat_id = text_data_json["chat_id"]
        sender = self.scope['user'].username

        # TODO: fazer assim pra no chat_message a gente conseguir enviar
        # a chave de "chat_id" pro front
        content: ChatMessage = {
            "type": "chat.message",
            "chat_id": chat_id,
            "sender": sender,
            "message": message
        }
        print("mensagem recebida, iniciando broadcast.\ncontent:" + content['message'])
        await self.channel_layer.group_send(chat_id, content)


    # aqui é quando o websocket recebe um evento do tipo chat.message no back
    async def chat_message(self, event: ChatMessage):
        # TODO: Acho que tem que mandar mais contexto nesse frame.
        # de repente mandar uma chave "chat_id", tipo assim:
        await self.send(text_data=json.dumps(event))


    async def remove_from_group(self, group_id: str):
        await self.channel_layer.group_discard(group_id, self.channel_name)
        self.dynamic_groups.remove(group_id)


    async def add_to_group(self, group_id: str):
        await self.channel_layer.group_add(group_id, self.channel_name)
        self.dynamic_groups.append(group_id)
