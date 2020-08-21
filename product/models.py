from django.db          import models

#1.카테고리테이블
class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

#2.서브 카테고리테이블
class SubCategory(models.Model):
    name        = models.CharField(max_length=45)
    category    = models.ForeignKey('Category',on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'


#3.상품테이블
class Product(models.Model):
    name            = models.CharField(max_length=45)
    price           = models.DecimalField(max_digits=20, decimal_places=2)
    sub_categories  = models.ForeignKey('SubCategory',on_delete=models.CASCADE)
    color           = models.ManyToManyField('Color',through='ProductColor')
    sizechart       = models.ManyToManyField('SizeChart',through='ProductSizeChart')
    size            = models.ManyToManyField('Size',through='ProductSize')
    
    class Meta:
        db_table = 'products'

#4.상품 색상 테이블
class Color(models.Model):
    name = models.CharField(max_length=45)

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
    image           = models.TextField(max_length=300)
    productcolor    = models.ForeignKey('ProductColor',on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'

#7. 상품사이즈 차트 테이블
class SizeChart(models.Model):
    table   = models.CharField(max_length=45)

    class Meta:
        db_table = 'size_charts'

#8. 사이즈 차트 테이블 ->중간테이블
class ProductSizeChart(models.Model):
    product     = models.ForeignKey('Product',on_delete=models.CASCADE)
    sizechart   = models.ForeignKey('SizeChart',on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_size_charts'

#9. 상품 사이즈 테이블
class Size(models.Model):
    size   = models.CharField(max_length=45)

    class Meta:
        db_table = 'sizes'

#10. 상품 사이즈 테이블 ->중간 테이블
class ProductSize(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    size    = models.ForeignKey('Size',on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_sizes'