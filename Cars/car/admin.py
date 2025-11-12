from django.contrib import admin
from .models import CarList, showroom, Review, CarImage, Booking
# Register your models here.
admin.site.register(CarList)
admin.site.register(showroom)
admin.site.register(Review)
admin.site.register(CarImage)
admin.site.register(Booking)
