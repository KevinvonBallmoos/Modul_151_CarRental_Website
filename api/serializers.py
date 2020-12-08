from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import Cars, Brand, Location, Customer, Rent
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CarSerializer(serializers.ModelSerializer):
    """
    Serialzer for the car model
    """
    brand_pks = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), source='brand', write_only=True,
                                                   label='Brand')
    image = serializers.ImageField(allow_null=True)

    def __init__(self, *args, **kwargs):
        """
        Overrides default constructor
        :param args: additionol parameter
        :param kwargs: additionol parameter
        """
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
    """
    Serializer for the brand model
    """
    car_list = CarSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'
        depth = 1


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Location model
    """

    class Meta:
        model = Location
        fields = '__all__'


class RentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rent model
    """
    customer_pk = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer',
                                                     write_only=True,
                                                     label='Customer')
    car_pk = serializers.PrimaryKeyRelatedField(queryset=Cars.objects.all(), source='car', write_only=True,
                                                many=True, label='Car')

    class Meta:
        model = Rent
        fields = '__all__'
        depth = 1

    def validate_car_pk(self, cars):
        """
        When no car_pks is selected the user gets a Error
        And when an car_pks is selected, its just valid if its not already in the car_list
        :param cars: cars
        :return: cars
        """
        if len(cars) == 0:
            raise serializers.ValidationError('No cars selected. Please select some cars to rent.')
        old_list = [] if not self.instance else self.instance.cars.all()
        for car in cars:
            if car not in old_list and car.is_rent:
                raise serializers.ValidationError(
                    'The Car "{}" with the ID "{}" is already rent.'.format(cars.title, cars.id)
                )
        return cars


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model
    """
    location_pk = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), source='location',
                                                     write_only=True,
                                                     label='Location')
    rent_list = RentSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}, 'email': {'required': True},
                        'first_name': {'required': True}, 'last_name': {'required': True}}

    def create(self, validated_data):
        """
        Checks if a email is already registered when creating a user
        :return: user
        """
        password = validated_data.pop('password', None)
        try:
            if User.objects.filter(email=validated_data.get('email')).exists():
                raise serializers.ValidationError('Email already registered.')
            password_validation.validate_password(password)
        except ValidationError as ve:
            raise serializers.ValidationError({'Password-Errors': [i for i in ve.messages]})
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Checks if a email is already registered when updating a user
        :param: instance actual user
        :return: super update method
        """
        if User.objects.filter(email=validated_data.get('email')).exists():
            user = User.objects.get(email=validated_data.get('email'))
            if instance != user:
                raise serializers.ValidationError('Email already registered.')
        return super(UserSerializer, self).update(instance, validated_data)
