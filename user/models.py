from django.db              import models

from .validation            import (
                    Validate_firstname,
                    Validate_lastname,
                    Validate_email,
                    Validate_password
)
class User(models.Model):
    firstname           = models.CharField(max_length = 100, validators = [Validate_firstname])
    lastname            = models.CharField(max_length = 100, validators = [Validate_lastname])
    email               = models.CharField(max_length = 100, validators = [Validate_email], unique = True)
    password            = models.CharField(max_length = 100, validators = [Validate_password])
    createdtime         = models.DateTimeField(auto_now_add = True)
    updatedtime         = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'users'
