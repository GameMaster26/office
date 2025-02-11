from django.core.management.base import BaseCommand
from monitoring.models import Treatment

class Command(BaseCommand):
    help = 'Populate empty vaccine fields in Treatment model with default values'

    def handle(self, *args, **options):
        # Define default values for the fields
        DEFAULT_GENERIC_NAME = 'PCECCV'
        DEFAULT_BRAND_NAME = 'Verorab'
        DEFAULT_ROUTE = 'intradermal'

        # Filter Treatments where any of the fields are blank or null
        treatments_to_update = Treatment.objects.filter(
            vaccine_generic_name__isnull=True
        ) | Treatment.objects.filter(
            vaccine_generic_name=''
        ) | Treatment.objects.filter(
            vaccine_brand_name__isnull=True
        ) | Treatment.objects.filter(
            vaccine_brand_name=''
        ) | Treatment.objects.filter(
            vaccine_route__isnull=True
        ) | Treatment.objects.filter(
            vaccine_route=''
        )

        if not treatments_to_update.exists():
            self.stdout.write(self.style.SUCCESS("No treatments with empty vaccine fields found."))
            return

        # Update each treatment with default values
        updated_count = 0
        for treatment in treatments_to_update:
            # Set default values only if fields are empty or null
            if not treatment.vaccine_generic_name:
                treatment.vaccine_generic_name = DEFAULT_GENERIC_NAME
            if not treatment.vaccine_brand_name:
                treatment.vaccine_brand_name = DEFAULT_BRAND_NAME
            if not treatment.vaccine_route:
                treatment.vaccine_route = DEFAULT_ROUTE
            treatment.save()
            updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully updated {updated_count} treatment records with default vaccine values."
        ))
