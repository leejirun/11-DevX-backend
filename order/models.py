from django.db      import models

from product.models import Product
from user.models    import User

class Order(models.Model):
    quantity      = models.CharField(max_length = 100)
    color         = models.CharField(max_length = 100, null=True)
    size          = models.CharField(max_length = 100, null=True)
    user          = models.ForeignKey(User, on_delete = models.CASCADE)
    product       = models.ForeignKey(Product, on_delete = models.CASCADE, null=True)
    
    class Meta:
        db_table = 'orders'

