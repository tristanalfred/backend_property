from rest_framework import serializers

from property_statistics.models import Property


class PropertySerializer(serializers.ModelSerializer):
    """
    Serializer allowing to insert a new property
    """
    class Meta:
        model = Property
        fields = ["price", "dept_code", "city", "zip_code"]


class PropertyStatSerializer(serializers.Serializer):
    """
    Serializer allowing to retrieve the statistics of properties in a certain sector
    """
    average = serializers.IntegerField()
    quantiles_10 = serializers.IntegerField()
    quantiles_90 = serializers.IntegerField()
