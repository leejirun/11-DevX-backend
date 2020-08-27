import re

from django.core.exceptions         import ValidationError

def Validate_firstname(firstname):
    firstname_reg = r"[ᄀ-힣a-zA-Z]{2,10}"
    regex         = re.compile(firstname_reg)
    
    if not regex.match(firstname):
        raise ValidationError('Firstname에 문자를 최소 2자 이상 입력해주세요.')

def Validate_lastname(lastname):
    lastname_reg = r"[ᄀ-힣a-zA-Z]{1,10}"
    regex        = re.compile(lastname_reg)  

    if not regex.match(lastname):
        raise ValidationError('Lastname에 문자를 최소 1자 이상 입력해주세요.')

def Validate_email(email):
    email_reg = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    regex     = re.compile(email_reg)

    if not regex.match(email):
        raise ValidationError('이메일 형식을 맞춰주세요.')
    
def Validate_password(password):
    if len(password) <= 5:
        raise ValidationError('비밀번호를 5자 이상을 입력하세요.')
