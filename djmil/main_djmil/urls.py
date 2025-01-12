from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path("main_page", views.MainPage.as_view(), name="main_page"),
    path('online_orders/', views.OnlineOrders.as_view(), name='online_orders'),
    path('online_second_orders/', views.OnlineSecondOrders.as_view(), name='online_second_orders'),
    path('online_second_orders_api/', views.OnlineSecondOrdersApi.as_view(), name='online_second_orders_api'),
    path('combat_orders/', views.CombatOrder.as_view(), name="combat_orders"),
    path('statistics/', views.StatisticsPage.as_view(), name='statistics'),
    path('flight_recorder/', views.FlightRecorder.as_view(), name='flight_recorder'),
    path('sky_safe/', views.SkySafeOrder.as_view(), name='sky_safe'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
    ]