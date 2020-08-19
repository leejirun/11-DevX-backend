from django.db import models

#1.카테고리테이블
class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'Categories'

#2.서브 카테고리테이블
class SubCategory(models.Model):
    name = models.CharField(max_length=45)
    category = models.ForeignKey('Category',on_delete=models.CASCADE)

    class Meta:
        db_table = 'SubCategories'


#4.상품 색상 테이블
class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'Colors'

#7. 상품사이즈 차트 테이블
class SizeChart(models.Model):
    size = models.CharField(max_length=45)
    length = models.CharField(max_length=45)
    width = models.CharField(max_length=45)

    class Meta:
        db_table = 'SizeCharts'

#9. 상품 사이즈 테이블
class Size(models.Model):
    size = models.CharField(max_length=45)

    class Meta:
        db_table = 'Sizes'


#3.상품테이블
class Product(models.Model):
    name = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sub_categories = models.ForeignKey('SubCategory',on_delete=models.CASCADE)
    color = models.ManyToManyField('Color',through='ProductColor')
    sizechart = models.ManyToManyField('SizeChart',through='ProductSizeChart')
    size = models.ManyToManyField('Size',through='ProductSize')
    
    class Meta:
        db_table = 'Products'



#5.상품 색상 ->중간 테이블
class ProductColor(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    color = models.ForeignKey('Color',on_delete=models.CASCADE)

    class Meta:
        db_table = 'ProductColors'

#6. 이미지 테이블====>상품 한개당 앞뒤이미지 어떻게 처리할거임??질문하기
class Image(models.Model):
    image = models.TextField(max_length=300)
    color = models.CharField(max_length=45)
    ProductColor = models.ForeignKey('ProductColor',on_delete=models.CASCADE)

    class Meta:
        db_table = 'Images'


#8. 사이즈 차트 테이블 ->중간테이블
class ProductSizeChart(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    SizeChart = models.ForeignKey('SizeChart',on_delete=models.CASCADE)

    class Meta:
        db_table = 'ProductSizeCharts'


#10. 상품 사이즈 테이블 ->중간 테이블
class ProductSize(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    size = models.ForeignKey('Size',on_delete=models.CASCADE)

    class Meta:
        db_table = 'ProductSizes'