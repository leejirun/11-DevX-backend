import json
from ast                    import literal_eval

from django.views           import View
from django.http            import JsonResponse

from .models                import Category, SubCategory, Product, Color, ProductColor
from .models                import Image, SizeChart, Size, ProductSize



class ProductMainView(View):
    def get(self, request):
        category_num = request.GET.get('category', None)
        products = Product.objects.filter(sub_category=category_num)
        body = {"category" : products[0].sub_category.name,
                "products" : []
         }
        for product in products :
            list_image = literal_eval(product.image_set.get(product=product).image)
            product_information = {
                "name"      : product.name,
                "price"     : product.price,
                "imageURL"  : [list_image[0], list_image[1]]
            }
            body["products"].append(product_information)
         
        return JsonResponse(body, status=200)
    

class ProductDetailView(View):
    def get(self, request, id) :
        body = {
            "products" : [],
            "pop-up products" : []
        }
        if Product.objects.filter(id=id).exists() :
            product        = Product.objects.get(id=id)
            list_image     = literal_eval(product.image_set.get(id=id).image)  
            mini_image = []
            for finder in list_image : 
                if "BACK" in list_image[0] and "BACK" in finder :
                    mini_image.append(finder)
                if "FRONT" in list_image[0] and "FRONT" in finder :
                    mini_image.append(finder)
            product_information = {
                "name"      : product.name,
                "imageURL"  : list_image,
                "price"     : product.price,
                "colors"    : [pc.color.name for pc in product.productcolor_set.filter(product=id)],
                "size"      : [sz.size.name for sz in product.productsize_set.filter(product=id)],
                "sizechart" : literal_eval(product.sizechart_set.get(id=id).table) 
            }
            mini_information = {
                "name"      : product.name,
                "imageURL"  : mini_image,
                "price"     : product.price,
                "colors"    : [pc.color.name for pc in product.productcolor_set.filter(product=id)]
            }
            body["products"].append(product_information)
            body["pop-up products"].append(mini_information)

        return JsonResponse(body, status=200)