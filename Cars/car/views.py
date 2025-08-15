from django.shortcuts import render
from django.http import JsonResponse
from .models import CarList
from serializerR.serializers import Carserializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
# def list_cars(request):
#     cars = CarList.objects.all()
#     data = {
#         'cars': list(cars.values())
#     }
#     return JsonResponse(data)

# def get_car(request, car_id):
#     try:
#         car = CarList.objects.get(id=car_id)
#         data = {
#             'name': car.name,
#             'model': car.model,
#             'year': car.year,
#             'price': str(car.price),
#             'active': car.Active
#         }
#         return JsonResponse(data)
#     except CarList.DoesNotExist:
#         return JsonResponse({'error': 'Car not found'}, status=404)
    


@api_view()
def list_cars(request):
    cars = CarList.objects.all()
    serializer = Carserializer(cars, many=True)
    return Response(serializer.data)

@api_view()
def get_car(request, car_id):
    try:
        car = CarList.objects.get(id=car_id)
        serializer = Carserializer(car)
        return Response(serializer.data)
    except CarList.DoesNotExist:
        return Response({'error': 'Car not found'}, status=404)