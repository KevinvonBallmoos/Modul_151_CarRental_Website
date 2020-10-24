from django.db import models


class CarLocation(models.Model):
    """
    CarLocation Model
    Basic-Model to store car locations
    """
    plz = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.location)


class Cars(models.Model):
    """
    Car-Model
    Basic-Model to store cars with image and details
    """
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    ps = models.IntegerField()
    details = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cars')
    location = models.ForeignKey(CarLocation, blank=True, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}{}'.format(self.brand, self.model)


class Location(models.Model):
    """
    Location-Model
    Basic-Model to store places
    """
    post_code = models.IntegerField(default=0)
    location = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}{}'.format(self.post_code, self.location)


class Customer(models.Model):
    """
    Customer-Model
    Basic-Model to store places
    """
    first_name = models.CharField(null=False, max_length=25)
    last_name = models.CharField(null=False, max_length=30)
    email = models.EmailField(null=False, max_length=50)
    street = models.CharField(null=False, max_length=25)
    phone_number = models.IntegerField(null=False)
    location = models.ForeignKey(Location, null=False, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}{}'.format(self.first_name, self.last_name)


class Rent(models.Model):
    """
    Rent-Model
    Basic-Model to store rents.
    Linked to customer with foreign-key.
    Linked to car location with many-to-many.
    """
    begin = models.DateField(null=False)
    rend = models.DateField(null=False, default=False)
    is_picked_up = models.BooleanField(null=False, default=False)
    is_returned = models.BooleanField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    car = models.ManyToManyField(Cars)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
