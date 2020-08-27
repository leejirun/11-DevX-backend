from django.test import TestCase, Client

from .models import Category, SubCategory, Product
from .models import Image, Color, ProductColor
from .models import SizeChart, Size, ProductSize

class ProductTest(TestCase):
    def setUp(self):
        client = Client()
        cate = Category.objects.create(name="men")
        subcate = SubCategory.objects.create(
            name="tshirt", 
            category=cate)
        prod =Product.objects.create(
            sub_category=subcate,
            name="spacex-tshirt",
            price="30.00"
            )
        Image.objects.create(
            product=prod,
            imageURL="www.naver.com",
            is_mainimage=1
            )
        color = Color.objects.create(
            name="black"
        )
        ProductColor.objects.create(
            product=prod,
            color=color
        )
        SizeChart.objects.create(
            product=prod,
            table="width=30"
        )
        sz = Size.objects.create(name="XL")
        ProductSize.objects.create(
            product=prod,
            size=sz
        )
    def tearDown(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        Image.objects.all().delete()
        Color.objects.all().delete()
        ProductColor.objects.all().delete()
        SizeChart.objects.all().delete()
        Size.objects.all().delete()
        ProductSize.objects.all().delete()

    def test_get_products_view(self):
       response =  self.client.get('/products?category=2')
       self.assertEqual(response.status_code, 200)
       self.assertEqual(response.json(), {
           "category" : "tshirt",
           "products" : [{
                        "name"      : "spacex-tshirt",
                        "price"     : "30.00",
                        "imageURL"  : ["www.naver.com"]
                        }]})

    def test_get_product_view(self):
       response =  self.client.get('/products/1')
       self.assertEqual(response.status_code, 200)
       self.assertEqual(response.json(), {
                "products" : [{
                    "product_id": 1,
                    "name"      : "spacex-tshirt",
                    "imageURL"  : ["www.naver.com"],
                    "price"     : "30.00",
                    "colors"    : ["black"],
                    "size"      : ["XL"],
                    "sizechart" : ["width=30"]
                    }],
                "pop-up products" : [{
                    "name"      : "spacex-tshirt",
                    "imageURL"  : ["www.naver.com"],
                    "price"     : "30.00",
                    "colors"    : ["black"]
                    }]
                    })
    