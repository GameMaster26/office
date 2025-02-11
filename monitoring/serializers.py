from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Barangay

class BarangayGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Barangay
        geo_field = 'boundary'  # This is the PolygonField
        fields = ('brgy_id', 'brgy_name', 'muni_id')  # Include the fields you want to serialize
