from rest_framework import serializers
from .models import Cars, Brand, Location, Customer, Rent


class CarSerializer(serializers.ModelSerializer):
    brand_pks = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), source='brand', write_only=True,
                                                   label='Cars')
    image = serializers.ImageField(allow_null=True)

    def __init__(self, *args, **kwargs):
        # Get additional parameters from constructor
        depth = kwargs.pop('depth', None)
        fields = kwargs.pop('fields', None)

        # Add author_pks to fields if field is not None from constructor
        fields.append('brand_pks') if fields is not None else None

        # Set Meta-Tags
        self.Meta.depth = depth if depth is not None else 1
        self.Meta.fields = fields if fields is not None else '__all__'

        # Call super-constructor
        super(CarSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Cars


class BrandSerializer(serializers.ModelSerializer):
    car_list = CarSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'
        depth = 1


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class RentSerializer(serializers.ModelSerializer):
    customer_pk = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer',
                                                     write_only=True,
                                                     label='Customer')
    car_pk = serializers.PrimaryKeyRelatedField(queryset=Cars.objects.all(), source='car', write_only=True,
                                                label='Car')

    class Meta:
        model = Rent
        fields = '__all__'
        depth = 1


class CustomerSerializer(serializers.ModelSerializer):
    location_pk = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), source='location',
                                                     write_only=True,
                                                     label='Location')
    rent_list = RentSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1
