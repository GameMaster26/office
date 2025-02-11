# monitoring/management/commands/remove_duplicates.py
from django.core.management.base import BaseCommand
from django.db import transaction
from monitoring.models import Treatment

class Command(BaseCommand):
    help = "Ensure each patient has only one treatment, and remove any extra treatments."

    def handle(self, *args, **kwargs):
        # Track the number of deleted duplicates
        duplicates_deleted = 0
        
        # Use a transaction to ensure data integrity
        with transaction.atomic():
            # Create a dictionary to track the first treatment per patient
            patient_treatments = {}

            # Iterate through all treatments
            for treatment in Treatment.objects.all():
                patient_id = treatment.patient_id  # Assuming patient_id is the unique identifier for the patient

                if patient_id not in patient_treatments:
                    # If the patient doesn't have a treatment yet, store the first one
                    patient_treatments[patient_id] = treatment
                else:
                    # If the patient already has a treatment, mark this one for deletion
                    treatment.delete()
                    duplicates_deleted += 1

        # Output the result
        self.stdout.write(self.style.SUCCESS(f"Deleted {duplicates_deleted} duplicate Treatment entries."))
