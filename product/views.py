import json
from django.views           import View
from django.http            import JsonResponse
from .models                import *
from ast import literal_eval

class TshirtView(View):
    def get(self, request):
        products = Product.objects.all()
        body = {
            "category" : "MEN'S T-SHIRT",
            "products" : []
            }
        for product in products:
            if product.id < 14 :
                imgs= Image.objects.get(product=product)
                list_image = literal_eval(imgs.image)
                new_list_image = []
                for i in range(2) :
                    new_list_image.append(list_image[i])
                name      = product.name
                price     = product.price
            
                tshirt_information = {
                    "name"      : name,
                    "price"     : price,
                    "imageURL"  : new_list_image,
                }
                body["products"].append(tshirt_information)
        return JsonResponse(body, status=200)

class OuterWearView(View):
    def get(self, request):
        products = Product.objects.all()
        body = {
            "category" : "MEN'S OUTERWEAR",
            "products" : []
            }
        for product in products:
            if product.id >= 14 :
                imgs= Image.objects.get(product=product)
                list_image = literal_eval(imgs.image)
                new_list_image = []
                for i in range(2) :
                    new_list_image.append(list_image[i])
                name      = product.name
                price     = product.price
        
                tshirt_information = {
                    "name"      : name,
                    "price"     : price,
                    "imageURL"  : new_list_image,
                }
                body["products"].append(tshirt_information)
        return JsonResponse(body, status=200)

class ProductDetailView(View):
    def get(self, request, id) :
        body = {
            "products" : [],
            "pop-up products" : []
        }
        if Product.objects.filter(id=id).exists() :
            product = Product.objects.get(id=id)
            imgs = Image.objects.get(product=id)
            list_image = literal_eval(imgs.image)
            szcht=SizeChart.objects.get(product=id)
            list_sizechart = literal_eval(szcht.table)    
            pcs = ProductColor.objects.filter(product=id)
            szs = ProductSize.objects.filter(product=id)
            
            sizes, colors, mini_image = [], [], []
            for pc in pcs:
                colors.append(pc.color.name)
            for sz in szs :
                sizes.append(sz.size.name)
            for finder in list_image : 
                if "BACK" in list_image[0] and "BACK" in finder :
                    mini_image.append(finder)
                if "FRONT" in list_image[0] and "FRONT" in finder :
                    mini_image.append(finder)
            print(list_image[0])
            product_information = {
                "name"      : product.name,
                "imageURL"  : list_image,
                "price"     : product.price,
                "colors"    : colors,
                "size"      : sizes,
                "sizechart" : list_sizechart
            }

            mini_information = {
                "name"      : product.name,
                "imageURL"  : mini_image,
                "price"     : product.price,
                "colors"    : colors
            }


            body["products"].append(product_information)
            body["pop-up products"].append(mini_information)

        return JsonResponse(body, status=200)