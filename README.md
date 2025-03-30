# chat_api

## 1. Models for the User Accounts:
**User**
Abstracting from the *django.contrib.auth.models.AbstractBaseUser*, the user account contains:
1. email: EmailField storing the email of the users.
- unique = True
- REQUIRED_FIELDS = True

2. name: CharField storing the name of the users.
- REQUIRED_FIELDS = True

3. avatar: ImageField storing the profile pic of the users.


## 2. Models for the Chat App:
**ChatRoom**
The ChatRoom model consists:
1. name: CharField storing the name of the chat rooms.
2. members: ManyToManyField storing the users in the chat room.
3. slug: SlugField that auto generates in the save method of the model instance with slugify and 5 randomly generated characters.

**Message**
The Message model consists:
1. room: ForeignKey to the ChatRoom
2. sender: ForeignKey to the User, which sends the message in the chatroom.
3. message: CharField storing the content of the message sent by the user. This can also be a TextField.

## 3. Django Channels setup:
`pip install channels channels-redis daphne`

1. Added channels and daphne to the INSTALLED_APPS:
```
INSTALLED_APPS = [
   'daphne',
   'channels',
   ...
]
```
2. Added `ASGI_APPLICATION = 'core.asgi.application'` in the settings.py.

3. Added
```
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # For development only
    }
}
```
This is InMemoryChannelLayer just for development but we should use RedisChannelLayer in production.

## 4. KnoxAuthentication Middleware:
*I am using Knox Authentication in the project.*
- Created the `KnoxAuthMiddleware` in the `middlewares.py` to connect websockets to the authenticated users only. If users are not authenticated, the websocket closes.

## 5. ChatConsumer
- Customized the `ChatConsumer` in `consumers.py` to manage the sending, receiving of messages and to store the chatroom messages.

## 6. Routing
- Finally, added `AuthMiddlewareStack`, `KnoxAuthMiddleware` under `ProtocolTypeRouter` with `websocket_urlpatterns` in `asgi.py`.

## 7. Websocket Connection and Testing:
- Tested the websocket with Postman and received and stored the messages sent in the chat rooms to the database.
