import bcrypt
import jwt 

from django.http           import JsonResponse
From django.http           import HttpResponse

from devx.settings         import SECRET_KEY
from devx.settings         import ALGORITHM
from .models               import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)         
            if access_token :                 
                payload         = jwt.decode(access_token, SECRET_KEY, algorithm = ALGORITHM)
                user            = User.objects.get(id = payload['user_id'])
                request.user    = user
                return func(self, request, *args, **kwargs)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status = 400)       
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 400)
    return wrapper

