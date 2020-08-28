import json

from django.views       import View
from django.http        import JsonResponse

from product.models     import Product
from user.models        import User
from user.decorator     import login_decorator
from .models            import Order

class OrderAddView(View):
    @login_decorator
    def post(self,request):
        data = json.loads(request.body)
        try:
            if Product.objects.filter(id = data['product_id']).exists(): 
                member  = User.objects.get(id = self.request.user.id)
                order_product = Product.objects.get(id = data['product_id'])               
                user_order = Order(
                    user   = member,
                    product = order_product,
                    color   = data['color'],
                    size    = data['size'],
                    quantity= data['quantity']
                )
                user_order.save()
                return JsonResponse({'message':'SUCCESS'}, status = 200)
            else:
                return JsonResponse({'message':'UNAUTHORIZED'}, status = 400)
        except Exception as exceptions: 
            return JsonResponse({'message':exceptions}, status = 400)

class OrderGetView(View):
    @login_decorator
    def get(self,request):
        
        result_list = []
        try:
            orders = Order.objects.filter(user=self.request.user.id).select_related('product').values('id','size','quantity','color','product__name','product__price','product_id').all()
            order_list = list(orders)
            for order in order_list:
                resultJson = order
                images = Product.objects.filter(id=order['product_id']).prefetch_related('image').values('image__image').get()
                order['image'] = images['image__image']
                result_list.append(order)
            return JsonResponse({'Order_list':result_list}, status = 200)
        except Exception as exceptions: 
            return JsonResponse({'message':exceptions}, status = 400)

class OrderDelView(View):
    @login_decorator
    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id = order_id)
            order.delete()
            return JsonResponse({'message':'SUCCESS'}, status = 200)
        except Exception as exceptions: 
            return JsonResponse({'message':exceptions}, status = 400)