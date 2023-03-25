from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path("main_page", views.MainPage.as_view(), name="main_page"),
    path("orders/", views.Orders.as_view(), name="orders"),
    path('second_orders/', views.SecondOrder.as_view(), name='second_order'),
    path('online_orders/', views.OnlineOrders.as_view(), name='online_orders'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
