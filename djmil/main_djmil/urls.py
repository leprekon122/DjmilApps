from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path("main_page", views.MainPage.as_view(), name="main_page"),
    path("orders/", views.Orders.as_view(), name="orders"),
    path('second_orders/', views.SecondOrder.as_view(), name='second_order'),
    path('online_orders/', views.OnlineOrders.as_view(), name='online_orders'),
    path('online_second_orders/', views.OnlineSecondOrders.as_view(), name='online_second_orders'),
    path('combat_orders/', views.CombatOrder.as_view(), name="combat_orders"),
    path('statistics/', views.StatisticsPage.as_view(), name='statistics'),
    path('flight_recorder/', views.FlightRecorder.as_view(), name='flight_recorder')

]
if settings.DEBUG:
    #urlpatterns += [static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    #                ]
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
    ]