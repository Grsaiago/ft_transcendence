from typing import List, TypedDict, Union
import json
from django.db.models import Q
import user_management.models as social_models
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import InMemoryChannelLayer
from channels_redis.core import RedisChannelLayer

class ChatMessage(TypedDict):
    type: str
    chat_id: str
    sender: str
    message: str

class ChatConsumer(AsyncWebsocketConsumer):
    groups: List[str] = ['general_chat']
    # essa variável vai ser usada para manter registro de quais
    # chats esse usuário tá inscrito, pra facilitar o cleanup no disconect
    dynamic_groups: List[str] = []
    # add some types to make development more sane
    channel_layer: Union[InMemoryChannelLayer, RedisChannelLayer]
    scope: dict


    async def connect(self):
        groups_to_add = social_models.Friendship.objects.filter(
            Q(first_user=self.scope['user'])
            | Q(second_user=self.scope['user'])
        ).values_list('chat_room_id', flat=True)

        for group in groups_to_add:
            await self.add_to_group(group)
        await self.accept()


    async def disconnect(self, code):
        for group in self.dynamic_groups:
            await self.remove_from_group(group)


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
