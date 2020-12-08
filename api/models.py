from django.db import models


class Brand(models.Model):
    """
    CarLocation Model
    Basic-Model to store car locations
    """
    brand = models.CharField(null=False, max_length=255)

    def __str__(self):
        return '{}'.format(self.brand)


class Cars(models.Model):
    """
    Car-Model
    Basic-Model to store cars with image and details
    """
    model = models.CharField(null=False, max_length=255)
    brand = models.ForeignKey(Brand, related_name='car_list', blank=False, on_delete=models.RESTRICT)
    ps = models.IntegerField()
    details = models.CharField(null=False, max_length=255)
    address = models.CharField(null=False, max_length=255)
    image = models.ImageField(null=False, upload_to='cars', default='noimage.png')
    is_rent = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.model, self.brand, )

    def save(self, *args, **kwargs):
        """
        When no image is set when creating a car, then a default image is set
        :param args: additional parameter
        :param kwargs: additional parameter
        """
        if not self.image:
            if self.id:
                self.image = Cars.objects.get(pk=self.id).image
            else:
                self.image = 'noimage.png'
        super().save(*args, **kwargs)


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
        return '{} {}'.format(self.post_code, self.location)


class Customer(models.Model):
    """
    Customer-Model
    Basic-Model to store places
    """
    first_name = models.CharField(null=False, max_length=25)
    last_name = models.CharField(null=False, max_length=30)
    email = models.EmailField(null=False, max_length=50)
    street = models.CharField(null=False, max_length=25)
    phone_number = models.CharField(null=False, max_length=25)
    location = models.ForeignKey(Location, null=False, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Rent(models.Model):
    """
    Rent-Model
    Basic-Model to store rents.
    Linked to customer with foreign-key.
    Linked to car location with many-to-many.
    """
    begin = models.DateField(null=False)
    end = models.DateField(null=False, default=False)
    is_picked_up = models.BooleanField(null=False, default=False)
    is_returned = models.BooleanField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    car = models.ManyToManyField(Cars, related_name='car_list', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, using=None, keep_parents=False):
        """
        When deleting a rent the is_rent attribute in the cars model gets the value false
        :param using:
        :param keep_parents:
        :return:
        """
        for car in self.car.all():
            car.is_rent = False
            car.save()
        super(Rent, self).delete()


def m2m_change_handler_for_rent_cars_through(sender, instance, action, **kwargs):
    """
    when a rent is created it adds it to the car_list
    :return: the rent in the car_list
    """
    if action == 'pre_remove' or action == 'pre_add':
        change_borrow_of_car_list(instance.cars.all(), False)
    elif action == 'post_remove' or action == 'post_add':
        change_borrow_of_car_list(instance.cars.all(), True)


def change_borrow_of_car_list(car_list: list, is_borrowed: bool):
    """
    when a rent gets in the car_list then the is_borrowed in rent gets the value true
    :param car_list:
    :param is_borrowed:
    :return:
    """
    for car in car_list:
        car.is_borrowed = is_borrowed
        car.save()
