from django.shortcuts import render
from django.http import JsonResponse
from .models import CarList, showroom, Review
from serializerR.serializers import Carserializer, ShowroomSerializer, ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
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
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        """
        Expect request.data to include the car id (key: 'car' or 'car_id').
        The URL provides showroom_pk so we validate the car belongs to that showroom.
        """
        def get_queryset(self):
            return Review.objects.all()
        
        showroom_pk = self.kwargs.get('showroom_pk')
        car_id = self.request.data.get('car') or self.request.data.get('car_id')
        useredit = self.request.user
        review_queryset = Review.objects.filter(car=car, api_user=useredit)
        if review_queryset.exists():
            raise ValidationError({'detail': 'You have already reviewed this car.'})
        if not car_id:
            raise ValidationError({'car': 'This field is required.'})

        try:
            car = CarList.objects.get(pk=car_id, showroom_id=showroom_pk)
        except CarList.DoesNotExist:
            raise ValidationError({'car': 'Car not found in this showroom.'})

        serializer.save(car=car, api_user=useredit)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """
        Return reviews for all cars in the given showroom (showroom_pk from URL).
        """
        showroom_pk = self.kwargs.get('showroom_pk')
        if showroom_pk is None:
            raise NotFound('showroom_pk not provided in URL.')
        return Review.objects.filter(car__showroom_id=showroom_pk)


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
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
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