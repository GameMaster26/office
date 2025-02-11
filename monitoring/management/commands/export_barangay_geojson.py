import os
from django.core.management.base import BaseCommand
from django.contrib.gis.serializers.geojson import Serializer as GeoJSONSerializer
from monitoring.models import Barangay

class Command(BaseCommand):
    help = 'Export Barangay boundaries to GeoJSON format'

    def add_arguments(self, parser):
        # Allow user to specify the output file path (optional)
        parser.add_argument(
            '--output',
            dest='output_file',
            default='Utro_na_sad.geojson',
            help='Specify the output file path for the GeoJSON data',
        )

    def handle(self, *args, **kwargs):
        # Get the output file path from the arguments
        output_file = kwargs.get('output_file')

        # Set the PROJ_LIB environment variable for GDAL
        os.environ['PROJ_LIB'] = r'C:\Program Files\PostgreSQL\16\share\contrib\postgis-3.4\proj'

        # Get all Barangays that have boundaries
        barangays = Barangay.objects.exclude(boundary=None)

        # Check if Barangays were found
        if not barangays:
            self.stdout.write(self.style.ERROR('No Barangays found with boundaries.'))
            return

        # Serialize data to GeoJSON format
        geojson_data = GeoJSONSerializer().serialize(barangays)

        # Write GeoJSON data to file using UTF-8 encoding
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(geojson_data)

            # Success message
            self.stdout.write(self.style.SUCCESS(f'Successfully exported Barangay boundaries to {output_file}'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to export Barangay boundaries: {e}'))