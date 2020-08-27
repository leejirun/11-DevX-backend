from django.test import TestCase, Client

from .models import Category, SubCategory, Product, Image

class ProductTest(TestCase):
    def setUp(self):
        client = Client()
        cate = Category.objects.create(name='men')
        subcate = SubCategory.objects.create(
            name='tshirt', 
            category=cate)
        prod =Product.objects.create(
            sub_category=subcate,
            name='spacex-tshirt',
            price='30.00'
            )
        Image.objects.create(
            product=prod,
            imageURL='www.naver.com',
            is_mainimage=1
            )

    def tearDown(self):
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        Image.objects.all().delete()

    def test_get_user_view(self):
       response =  self.client.get('/products?category=1')
       self.assertEqual(response.status_code, 200)
       self.assertEqual(response.json(), {
           "category" : "tshirt",
           "products" : [{
                        "name"      : 'spacex-tshirt',
                        "price"     : '30.00',
                        "imageURL"  : ['www.naver.com']
                        }]})