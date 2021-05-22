from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.register, name="register"),
    path('login', views.loginpage, name="login"),
    path('logout', views.logoutuser, name="logout"),

    path('', views.home, name="home"),
    path('user', views.userpage, name="user_page"),
    path('product', views.products, name="product"),
    path('costumer/<str:pk>/', views.customer, name="costumer"),
    path('createOrder/<str:pk>/', views.createOrder, name="create_order"),
    path('UpdateOrder/<str:pk>/', views.update_Order, name="Update_order"),
    path('Delete_order/<str:pk>/', views.delete_order, name="Delete_order")

]
