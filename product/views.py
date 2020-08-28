import json
from ast                    import literal_eval

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Prefetch

from .models                import Category, SubCategory, Product, Color, ProductColor
from .models                import Image, SizeChart, Size, ProductSize

class ProductsView(View):
    def get(self, request):
        category_num     = request.GET.get('category', None)
        products         = Product.objects.prefetch_related('image_set').filter(sub_category=category_num)
        if products :
            body = {"category" : products.first().sub_category.name,
                    "products" : [{
                        "name"      : product.name,
                        "price"     : product.price,
                        "imageURL"  : [image.imageURL for image in product.image_set.all() if image.is_mainimage==1]
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
            list_image    = [image.imageURL for image in product.image_set.all()]
            body = {
                "products" : [{
                    "product_id": id,
                    "name"      : product.name,
                    "imageURL"  : list_image,
                    "price"     : product.price,
                    "colors"    : [pc.name for pc in product.to_color],
                    "size"      : [sz.name for sz in product.to_size],
                    "sizechart" : [sz.table for sz in product.sizechart_set.all()] 
                    }],
                "pop-up products" : [{
                    "name"      : product.name,
                    "imageURL"  : [list_image[i] for i in range(0, len(list_image), 2)],
                    "price"     : product.price,
                    "colors"    : [pc.name for pc in product.to_color]
                    }]
            }
            return JsonResponse(body, status=200)
        return JsonResponse({"message":"Invalid Product Number!!"}, status = 400)