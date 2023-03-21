from django.urls import path
from . import views
urlpatterns = [
   path('', views.login_page, name='login'),
   path("main_page", views.MainPage.as_view(), name="main_page"),
   path("orders/", views.Orders.as_view(), name="orders")

]