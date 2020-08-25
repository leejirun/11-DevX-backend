from django.urls import path

from .views      import ProductMainView, ProductDetailView

urlpatterns = [
    path('/main', ProductMainView.as_view()),
    path('/detail/<int:id>', ProductDetailView.as_view()),
]
