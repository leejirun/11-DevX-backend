from django.urls    import path

from .views         import OrderAddView
from .views         import OrderGetView
from .views         import OrderDelView

urlpatterns = [
    path('/add',OrderAddView.as_view()),
    path('/del/<int:order_id>',OrderDelView.as_view()),
    path('/', OrderGetView.as_view()),
]
