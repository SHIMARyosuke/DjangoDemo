from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
'''LoginView, LogoutViewクラスベースビューを使用する'''
urlpatterns = [
    path('login/', LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='accounts/login.html'
        ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
