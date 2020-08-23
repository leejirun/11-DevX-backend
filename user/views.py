import json,traceback
import bcrypt #pip install bcrypt
import jwt #pip install pyJWT 

from .models                import User
from devx.settings          import SECRET_KEY
from datetime import datetime

from django.views           import View
from django.http            import JsonResponse,HttpResponse
from django.core.exceptions import ValidationError
from .validation            import Validate_firstname
from .decorator             import login_decorator



class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            #비밀                                            번호 암호화
            password        = data['password'].encode('utf-8')
            password_crypt  = bcrypt.hashpw(password,bcrypt.gensalt())
            password_crypt  = password_crypt.decode('utf-8')
            #끝 
            req_User = User(
                firstname  = data['firstname'],
                lastname   = data['lastname'],
                email      = data['email'],
                password   = password_crypt,
            )
            req_User.full_clean() #유효성 검사
            req_User.save() #db에 저장
        except ValidationError as exceptions: #{'firstname' : ['두개 이상 쓰세요..'], 'email' : ['이미 있음..']}
            print(exceptions)
            msgs = ''
            for msg in dict(exceptions).values(): #dict-> values = [ ['두개 이상 쓰세요..'], ['이미 있음..'] ]
                msgs += msg[0] + ' / ' #msg = ['두개 이상 쓰세요..'] -> msg[0] = '두개 이상 쓰세요..'
            return JsonResponse({'message':msgs[:-3]},status = 400)
        except KeyError as exceptions: 
            return JsonResponse({'message':'KEY ERROR'}, status = 401)
        return JsonResponse({'message':'SUCCESS'},status = 200)

class SignInView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if User.objects.all().filter(email = data['email']).exists() :
                user = User.objects.get(email = data['email'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')) :
                    #토큰발행
                    token = jwt.encode({'email': data['email']}, SECRET_KEY,algorithm="HS256")
                    token = token.decode('utf-8')
                    return JsonResponse({'message':"SUCCESS","token":token},status=200)
            return JsonResponse({'message':'PASSWORD ERROR'},status = 401) 
        except KeyError:
            return JsonResponse({'message':'KEYERROR'},status = 400)       
    
