from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('ViewDetails/<id>',views.ViewDetails),
    path('login',views.login),
    path('signout',views.signout),
    path('ShowPrdt/<id>',views.ShowPrdt),
    path('addToCart',views.addToCart),
    path('ShowAllCartItems',views.ShowAllCartItems),
    path('RemoveItem',views.RemoveItem),
    path('MakePayment',views.MakePayment),
    path('verify',views.verify),
    path('register',views.register),
    #path('MyOrders',views.MyOrders),
    path('addr',views.addr),
    path('myorder',views.myorder),
]