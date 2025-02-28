from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from knox.models import AuthToken
from django.contrib.auth.models import AnonymousUser


class KnoxAuthMiddleware:
    def __init__(self, inner):
        """
        Args:
            inner: The next middleware or consumer in the stack.       
        """
        self.inner = inner


    async def __call__(self, scope, receive, send):
        """
        Args:
            scope (dict): The connection scope, containing request details.
            receive (callable): Function to receive messages from the WebSocket.
            send (callable): Function to send messages to the WebSocket.
        """
        # Extract token from the query strings or headers
        token = self.get_token_from_scope(scope)

        # Authenticate user based on the extracted token
        scope["user"] = await self.get_user(token)

        # Pass the modified scope to the next middleware/consumer
        return await self.inner(scope, receive, send)


    def get_token_from_scope(self, scope):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        if not token:
            headers = dict(scope.get("headers", []))
            token = headers.get(b'authorization', b'').decode().replace("Token ", "").strip()
        
        return token
    

    @database_sync_to_async
    def get_user(self, token):
        if not token:
            return AnonymousUser()
        
        try:
            auth_token = AuthToken.objects.filter(token_key=token[:15]).first()

            if auth_token and auth_token.user:
                return auth_token.user
            
        except AuthToken.DoesNotExist:
            pass

        print(auth_token)

        return AnonymousUser()