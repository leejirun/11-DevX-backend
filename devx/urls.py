from django.urls        import path,include

urlpatterns = [
    path('user', include('user.urls')),
    path('', ProductsView.as_view()),
    path('/<int:id>', ProductView.as_view()),
    path('order', include('order.urls'))
]

