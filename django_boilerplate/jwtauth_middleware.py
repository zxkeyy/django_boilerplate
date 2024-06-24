from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

class JWTAuthMiddleware(BaseMiddleware):
    
    async def __call__(self, scope, receive, send):
    
        token = self.get_token_from_scope(scope)
        
        if token != None:
            user = await self.get_user_from_token(token) 
            if user:
                scope['user'] = user

            else:
                scope['error'] = 'Invalid token'

        if token == None:
            scope['error'] = 'provide an auth token'    
    
                
        return await super().__call__(scope, receive, send)

    def get_token_from_scope(self, scope):
        headers = dict(scope.get("headers", []))
        
        auth_header = headers.get(b'authorization', b'').decode('utf-8')
        
        if auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        
        else:
            return None
        
    @database_sync_to_async
    def get_user_from_token(self, token):
            try:
                access_token = AccessToken(token)
                user = get_user_model().objects.get(id=access_token['user_id'])
                return user
            except Exception as e:
                print(e)
                return None