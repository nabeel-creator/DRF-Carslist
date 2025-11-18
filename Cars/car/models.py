from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
def chassivalidator(value):
    if not str(value).isalnum():
        raise ValidationError("Chassis number must be alphanumeric.")
    return value


class showroom(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class CarList(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Active = models.BooleanField(default=True)
    features = models.JSONField(null=True, blank=True)  
    description = models.TextField(null=True, blank=True)
    chassinumber = models.CharField(max_length=100, null=True, blank=True, validators=[chassivalidator])
    showroom = models.ForeignKey("showroom", on_delete=models.CASCADE, null=True, related_name="cars")

    def __str__(self):
        return f"{self.name} - {self.model}"

class CarImage(models.Model):
    car = models.ForeignKey(CarList, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="car_images/")

    def __str__(self):
        return f"Image for {self.car.name}"


class Review(models.Model):
    car = models.ForeignKey(CarList, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    api_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"Review for {self.car.name} -- Rating: {self.rating}"


class Booking(models.Model):
    car = models.ForeignKey(CarList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    