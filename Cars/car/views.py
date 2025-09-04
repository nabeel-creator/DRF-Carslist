from django.shortcuts import render
from django.http import JsonResponse
from .models import CarList
from serializerR.serializers import Carserializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
    


@api_view(['GET', 'POST'])
def list_cars(request):
    if request.method == 'GET':
        cars = CarList.objects.all()
        serializer = Carserializer(cars, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = Carserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def get_car(request, car_id):
    if request.method == 'GET':
        try:
            car = CarList.objects.get(id=car_id)
            serializer = Carserializer(car)
            return Response(serializer.data)
        except CarList.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        try:
            car = CarList.objects.get(id=car_id)
            serializer = Carserializer(car, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CarList.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        try:
            car = CarList.objects.get(id=car_id)
            car.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CarList.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)