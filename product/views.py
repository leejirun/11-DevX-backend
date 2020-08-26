import json
from ast                    import literal_eval

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Prefetch

from .models                import Category, SubCategory, Product, Color, ProductColor
from .models                import Image, SizeChart, Size, ProductSize



class ProductsView(View):
    def get(self, request):
        category_num = request.GET.get('category', None)
        products = Product.objects.prefetch_related('image_set').filter(sub_category=category_num)
        if products :
            body = {"category" : products[0].sub_category.name,
                    "products" : [{
                        "name"      : product.name,
                        "price"     : product.price,
                        "imageURL"  : [literal_eval(product.image_set.get(product=product).image)[i] for i in range(2)]
                        } for product in products]
                    }
            return JsonResponse(body, status=200)
        return JsonResponse({"Message" : "Invalid Category Number!!"}, status=400)
    
class ProductView(View):
    def get(self, request, id) :
        if Product.objects.prefetch_related('image_set').filter(id=id).exists() :
            product        = Product.objects.prefetch_related(
                Prefetch('color', to_attr='to_color')).prefetch_related(
                    Prefetch('size', to_attr='to_size')).get(id=id)
            list_image     = literal_eval(product.image_set.get(id=id).image) 
            if "BACK" in list_image[0] :
                images     = [image for image in list_image if "BACK" in image]
            elif "FRONT" in list_image[0] :
                images     = [image for image in list_image if "FRONT" in image]
            body = {
                "products" : [{
                    "product_id": id,
                    "name"      : product.name,
                    "imageURL"  : list_image,
                    "price"     : product.price,
                    "colors"    : [pc.name for pc in product.to_color],
                    "size"      : [sz.name for sz in product.to_size],
                    "sizechart" : literal_eval(product.sizechart_set.get(id=id).table) 
                    }],
                "pop-up products" : [{
                    "name"      : product.name,
                    "imageURL"  : images,
                    "price"     : product.price,
                    "colors"    : [pc.name for pc in product.to_color]
                    }]
            }
            return JsonResponse(body, status=200)
        return JsonResponse({"message":"Invalid Product Number!!"}, status = 400)
