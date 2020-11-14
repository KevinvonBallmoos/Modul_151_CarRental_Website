from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import CarSerializer, BrandSerializer, LocationSerializer, CustomerSerializer, RentSerializer, UserSerializer
from .models import Cars, Brand, Location, Customer, Rent
from .permissions import IsAuthenticatedOrPostOnly
from django.contrib.auth.models import User


class CarViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Cars.objects.all().order_by('model')
    serializer_class = CarSerializer


class BrandViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Brand.objects.all().order_by('brand')
    serializer_class = BrandSerializer


class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Location.objects.all().order_by('location')
    serializer_class = LocationSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Customer.objects.all().order_by('first_name')
    serializer_class = CustomerSerializer


class RentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Rent.objects.all().order_by('begin')
    serializer_class = RentSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrPostOnly]

    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
