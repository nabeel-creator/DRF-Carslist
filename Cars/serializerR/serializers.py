from rest_framework import serializers

class Carserializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    model = serializers.CharField(max_length=100)
    year = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    active = serializers.BooleanField(default=True)

