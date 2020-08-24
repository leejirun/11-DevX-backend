from django.urls import path

from .views      import *

urlpatterns = [
    path('/tshirt', TshirtView.as_view()),
    path('/outerwear', OuterWearView.as_view()),
    path('/detail/<int:id>', ProductDetailView.as_view()),
    # path('/test', TestView.as_view())
]
