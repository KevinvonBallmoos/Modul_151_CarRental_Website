from rest_framework import routers
from django.urls import path, include
from . import views as api_views
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

routers = routers.DefaultRouter()
routers.register(r'cars', api_views.CarViewSet)
routers.register(r'brand', api_views.BrandViewSet)
routers.register(r'location', api_views.LocationViewSet)
routers.register(r'customer', api_views.CustomerViewSet)
routers.register(r'rent', api_views.RentViewSet)
routers.register(r'user', api_views.UserViewSet)


urlpatterns = [
    path('', include(routers.urls)),
    path('api-auth-token/', obtain_auth_token),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc-ui', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui')
]
