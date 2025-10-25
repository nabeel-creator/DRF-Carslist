from rest_framework import serializers
from car.models import CarList, showroom, Review
from decimal import Decimal


class ReviewSerializer(serializers.ModelSerializer):
    api_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        # exclude = ('car',)


class ShowroomSerializer(serializers.ModelSerializer):
    showrooms = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    class Meta:
        model = showroom
        fields = '__all__'

class Carserializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()
    class Meta:
        model = CarList
        fields = '__all__'
        # exclude = ['id']
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=100)
    # model = serializers.CharField(max_length=100)
    # year = serializers.IntegerField()
    # price = serializers.DecimalField(max_digits=10, decimal_places=2)
    # Active = serializers.BooleanField(default=True)
    # chassinumber = serializers.CharField(max_length=100, validators=[chassivalidator])

    # def create(self, validated_data):
    #     return CarList.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name',instance.name)
    #     instance.model = validated_data.get('model',instance.model)
    #     instance.year = validated_data.get('year',instance.year)
    #     instance.price = validated_data.get('price',instance.price)
    #     instance.Active = validated_data.get('Active',instance.Active)
    #     instance.save()
    #     return instance
    def get_discounted_price(self, obj):
        if obj.price > Decimal('11500000.00'):
            return obj.price * Decimal('0.9')  # 10% discount
        return obj.price
    def validate_price(self, value):
        if value <= 100000:
            raise serializers.ValidationError("Price must be greater than 1 lakh.")
        return value

    def validate(self, data):
        if data['name'] == data['model']:
            raise serializers.ValidationError("Name and model must be different.")
        return data