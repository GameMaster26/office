# monitoring/management/commands/add_missing_histories.py

from django.core.management.base import BaseCommand
from django.db import transaction
from monitoring.models import Patient, History, Municipality, Barangay
from datetime import date

class Command(BaseCommand):
    help = "Ensure that every patient has one history record. Adds a default history if missing."

    def handle(self, *args, **kwargs):
        # Track how many histories were added
        histories_added = 0

        # Use a transaction to ensure data integrity
        with transaction.atomic():
            # Fetch the default Municipality and Barangay (or set your own logic)
            # Here, we're fetching the first ones, you might want to change this depending on your logic
            default_municipality = Municipality.objects.first()  # Adjust this if needed
            default_barangay = Barangay.objects.first()  # Adjust this if needed

            # Check if default Municipality and Barangay exist
            if not default_municipality or not default_barangay:
                self.stdout.write(self.style.ERROR("Default Municipality or Barangay not found."))
                return

            # Iterate through all patients
            for patient in Patient.objects.all():
                # Check if this patient already has a history
                if not History.objects.filter(patient_id=patient).exists():
                    # If no history exists for the patient, create a default history record
                    self.create_default_history(patient, default_municipality, default_barangay)
                    histories_added += 1

        # Output the result
        self.stdout.write(self.style.SUCCESS(f"Added {histories_added} missing history records."))

    def create_default_history(self, patient, default_municipality, default_barangay):
        # Create a default History for the patient
        # Here, we use the actual instances of Municipality and Barangay
        default_history = History(
            patient_id=patient,
            date_registered=date.today(),  # You can set this to the current date
            date_of_exposure=date.today(), # Default date of exposure (or you can set it to None)
            muni_id=default_municipality,  # Use the default municipality instance
            brgy_id=default_barangay,      # Use the default barangay instance
            category_of_exposure='II',     # Default to category II or any category you prefer
            source_of_exposure='Dog',      # Default source of exposure
            exposure_type='Bite',          # Default exposure type
            bite_site='Front of Head',     # Set a default bite site or other valid choices
            provoked_status='Unprovoked',  # Set a default provocation status
            immunization_status='Unimmunized',  # Default immunization status
            status_of_animal='Lost',       # Set a default status of animal
            confinement_status='Stray',    # Default confinement status
            washing_hands='Yes',           # Default washing status
            human_rabies=False,            # Default human rabies status
            latitude=0.0,                  # Default latitude
            longitude=0.0,                 # Default longitude
            geom=None,                     # Default geometry point
        )

        # Save the default history
        default_history.save()
