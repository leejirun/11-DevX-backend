from django.db          import models

#1.카테고리테이블
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

#2.서브 카테고리테이블
class SubCategory(models.Model):
    category    = models.ForeignKey('Category',on_delete=models.CASCADE)
    name        = models.CharField(max_length=100)

    class Meta:
        db_table = 'sub_categories'

#3.상품테이블
class Product(models.Model):
    sub_category    = models.ForeignKey('SubCategory',on_delete=models.CASCADE)
    name            = models.CharField(max_length=100)
    price           = models.DecimalField(max_digits=50, decimal_places=2)
    color           = models.ManyToManyField('Color',through='ProductColor')
    size            = models.ManyToManyField('Size',through='ProductSize')
    
    class Meta:
        db_table = 'products'

#4.상품 색상 테이블
class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'colors'

#5.상품 색상 ->중간 테이블
class ProductColor(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    color   = models.ForeignKey('Color',on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_colors'

#6. 이미지 테이블
class Image(models.Model):
    product      = models.ForeignKey('Product',on_delete=models.CASCADE)
    imageURL     = models.URLField(max_length=2000)
    is_mainimage = models.BooleanField()


    class Meta:
        db_table = 'images'

#7. 상품사이즈 차트 테이블
class SizeChart(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    table   = models.CharField(max_length=1000, null=True)
    
    class Meta:
        db_table = 'size_charts'

#8. 상품 사이즈 테이블
class Size(models.Model):
    name    = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'sizes'

#9. 상품 사이즈 ->중간 테이블
class ProductSize(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    size    = models.ForeignKey('Size',on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_sizes'