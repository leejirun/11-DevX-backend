import json,traceback
import bcrypt 
import jwt 

from .models                        import User
from devx.settings                  import SECRET_KEY
from devx.settings                  import ALGORITHM
from datetime                       import datetime

from django.views                   import View
from django.http                    import JsonResponse,HttpResponse
from django.core.exceptions         import ValidationError
from .validation                    import Validate_firstname
from .validation                    import Validate_lastname
from .validation                    import Validate_email
from .validation                    import Validate_password
from .decorator                     import login_decorator



class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            password        = data['password'].encode('utf-8')
            password_crypt  = bcrypt.hashpw(password,bcrypt.gensalt())
            password_crypt  = password_crypt.decode('utf-8')
            req_User = User(
                firstname  = data['firstname'],
                lastname   = data['lastname'],
                email      = data['email'],
                password   = password_crypt,
            )
            req_User.full_clean() 
            req_User.save() 
        except ValidationError as exceptions: 
            print(exceptions)
            msgs = ''
            for msg in dict(exceptions).values(): 
                msgs += msg[0] + ' / ' 
            return JsonResponse({'message':msgs[:-3]},status = 400)
        except KeyError as exceptions: 
            return JsonResponse({'message':'KEY ERROR'}, status = 401)
        return JsonResponse({'message':'SUCCESS'},status = 200)

class SignInView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email = data['email']).exists() :
                user = User.objects.get(email = data['email'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'user_id': user.id}, SECRET_KEY,algorithm=ALGORITHM)
                    token = token.decode('utf-8')
                    return JsonResponse({'message':"SUCCESS","token":token},status=200)
            return JsonResponse({'message':'PASSWORD ERROR'},status = 401) 
        except KeyError:
            return JsonResponse({'message':'KEYERROR'},status = 400)       
    
