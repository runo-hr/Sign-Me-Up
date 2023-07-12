from rest_framework.authtoken.models import Token

from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()


class TokenExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Authorization' in request.headers:
            print('Authorized')
            auth_header = request.headers['Authorization']
            token_key = auth_header.split(' ')[1]  # Extract the token from the Authorization header
            print(f'token_key: {token_key}')
            try:
                token = Token.objects.get(key=token_key)

                if token.created < timezone.now() - timezone.timedelta(days=5):
                    token.delete() # Token has expired, delete it
                    response_data = {'message': 'Token has expired. Please log in again.'}
                    return JsonResponse(response_data, status=401)
                else:
                    # Update token's created time to extend its expiration
                    token.created = timezone.now()
                    token.save()
            
            except Token.DoesNotExist:
                print('Token.DoesNotExist')
                response_data = {
                    'message': 'Invalid token'
                }
                return JsonResponse(response_data, status=401)

        response = self.get_response(request)
        return response
