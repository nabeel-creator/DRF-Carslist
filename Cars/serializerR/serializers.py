from rest_framework import serializers
from car.models import CarList

def chassivalidator(value):
    if str(value).isalnum():
        raise serializers.ValidationError("Chassis number must be alphanumeric.")
    return value

class Carserializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    model = serializers.CharField(max_length=100)
    year = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    Active = serializers.BooleanField(default=True)
    chassinumber = serializers.CharField(max_length=100, validators=[chassivalidator])

    def create(self, validated_data):
        return CarList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.model = validated_data.get('model',instance.model)
        instance.year = validated_data.get('year',instance.year)
        instance.price = validated_data.get('price',instance.price)
        instance.Active = validated_data.get('Active',instance.Active)
        instance.save()
        return instance

    def validate_price(self, value):
        if value <= 100000:
            raise serializers.ValidationError("Price must be greater than 1 lakh.")
        return value

    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and description must be different.")
        return data