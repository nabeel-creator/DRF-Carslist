from django.shortcuts import render
from django.http import JsonResponse
from .models import CarList, showroom, Review, Booking
from serializerR.serializers import Carserializer, ShowroomSerializer, ReviewSerializer, BookingSerializer
from serializerR.permissions import isOwnerOrReadOnly, adminorReadonly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound

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

class UserBookingList(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingCreate(generics.CreateAPIView):
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [isOwnerOrReadOnly]

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        showroom_pk = self.kwargs.get('showroom_pk')
        car_id = self.request.data.get('car') or self.request.data.get('car_id')
        user = self.request.user

        if not car_id:
            raise ValidationError({'car': 'This field is required.'})

        # Make sure the car belongs to this showroom
        try:
            car = CarList.objects.get(pk=car_id, showroom_id=showroom_pk)
        except CarList.DoesNotExist:
            raise ValidationError({'car': 'Car not found in this showroom.'})

        # Prevent duplicate review from same user for the same car
        if Review.objects.filter(car=car, api_user=user).exists():
            raise ValidationError({'detail': 'You have already reviewed this car.'})

        serializer.save(car=car, api_user=user)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        showroom_pk = self.kwargs.get('showroom_pk')
        car_id = self.request.query_params.get('car_id', None)

        queryset = Review.objects.filter(car__showroom_id=showroom_pk)

        if car_id:
            queryset = queryset.filter(car_id=car_id)

        return queryset

# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin, 
#                  generics.GenericAPIView):

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)



class showroom_view(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isOwnerOrReadOnly]
    queryset = showroom.objects.all()
    serializer_class = ShowroomSerializer

# class showroom_view(viewsets.ViewSet):
#     def list(self, request):
#         showrooms = showroom.objects.all()
#         serializer = ShowroomSerializer(showrooms, many=True, context={'request': request})
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         try:
#             showroom_instance = showroom.objects.get(pk=pk)
#             serializer = ShowroomSerializer(showroom_instance)
#             return Response(serializer.data)
#         except showroom.DoesNotExist:
#             return Response({'error': 'Showroom not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     def create(self, request):
#         serializer = ShowroomSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class showroomList(APIView):

    def get(self, request):
        showrooms = showroom.objects.all()
        serializer = ShowroomSerializer(showrooms, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ShowroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class showroom_details(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [adminorReadonly]
    def get(self, request, pk):
        try:
            showroom_instance = showroom.objects.get(pk=pk)
            serializer = ShowroomSerializer(showroom_instance)
            return Response(serializer.data)
        except showroom.DoesNotExist:
            return Response({'error': 'Showroom not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            showroom_instance = showroom.objects.get(pk=pk)
            serializer = ShowroomSerializer(showroom_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except showroom.DoesNotExist:
            return Response({'error': 'Showroom not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            showrooms = showroom.objects.get(pk=pk)
            showrooms.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except showroom.DoesNotExist:
            return Response({'error': 'Showroom not found'}, status=status.HTTP_404_NOT_FOUND)






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