from rest_framework import routers
from django.urls import path, include
from . import views as api_views

routers = routers.DefaultRouter()
routers.register(r'cars', api_views.CarViewSet)
routers.register(r'brand', api_views.BrandViewSet)
routers.register(r'location', api_views.LocationViewSet)
routers.register(r'customer', api_views.CustomerViewSet)
routers.register(r'rent', api_views.RentViewSet)


urlpatterns = [
    path('', include(routers.urls)),
    path('api-auth', include('rest_framework.urls'))
]
