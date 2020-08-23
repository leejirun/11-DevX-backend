from django.urls    import path
from .views        import SignUpView,SignInView,SignOutView

urlpatterns = [
    path('/up',SignUpView.as_view()),
    path('/in',SignInView.as_view())
    
]
