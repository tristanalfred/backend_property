import os
import requests

from math import floor

from django.db.models import Avg
from rest_framework import viewsets, status
from rest_framework.response import Response

from backend_property.settings import URL_BIENICI_PROPERTY
from property_statistics.models import Property
from property_statistics.serializers import PropertyStatSerializer, PropertySerializer


# Create your views here.
class StatisticsViewSet(viewsets.ViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertyStatSerializer

    def retrieve(self, request, *_args, **kwargs):
        # Retrieve the useful information in the request
        localisation_type = request.query_params["localisation_type"]
        search_value = kwargs["search_value"]

        # Filter by the correct attribute
        if localisation_type == "dept_code":
            considered_properties = Property.objects.filter(dept_code=search_value).order_by('price')
        elif localisation_type == "city":
            considered_properties = Property.objects.filter(city=search_value).order_by('price')
        elif localisation_type == "zip_code":
            considered_properties = Property.objects.filter(zip_code=search_value).order_by('price')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Calculate the statistical datas
        average_value = list(considered_properties.aggregate(Avg('price')).values())[0]
        quantile_10 = considered_properties[floor(len(considered_properties)/10)].price
        quantile_90 = considered_properties[floor(len(considered_properties) - len(considered_properties)/10)].price

        # Return the formatted data
        stat_data = {"average": average_value,
                     "quantiles_10": quantile_10,
                     "quantiles_90": quantile_90}

        results = PropertyStatSerializer(stat_data).data
        return Response(results)


class PropertyUrlViewSet(viewsets.ViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def create(self, _request, *_args, **kwargs):
        api_url = URL_BIENICI_PROPERTY
        id_property = kwargs["url"]

        # Search for Bienici's ad through the url
        try:
            response = requests.get(api_url + os.path.basename(id_property))
        except Exception:
            return Response(status.HTTP_404_NOT_FOUND)

        if not response:
            return Response(status.HTTP_404_NOT_FOUND)

        # Store the data
        property_data = {"price": response.json()["price"],
                         "dept_code": response.json()["postalCode"][:-3],
                         "city": response.json()["city"],
                         "zip_code": response.json()["postalCode"]}
        serializer = PropertySerializer(data=property_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status.HTTP_201_CREATED)
        return Response(status.HTTP_404_NOT_FOUND)
