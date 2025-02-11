from django.core.management.base import BaseCommand
from monitoring.models import Patient, Doctor, User, Treatment

class Command(BaseCommand):
    help = 'Assign a specific doctor to all treatments for patients associated with a specific user'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='User ID to update treatments for')
        parser.add_argument('doctor_id', type=int, help='Doctor ID to assign to treatments')

    def handle(self, *args, **options):
        user_id = options['user_id']
        doctor_id = options['doctor_id']

        try:
            # Fetch the doctor and user by their IDs
            doctor = Doctor.objects.get(id=doctor_id)
            user = User.objects.get(id=user_id)

            # Get all patients associated with the specified user
            patients = Patient.objects.filter(user=user)

            if not patients.exists():
                self.stdout.write(self.style.WARNING(f"No patients found for user with ID {user_id}."))
                return

            # Get all treatments for patients associated with this user
            treatments = Treatment.objects.filter(patient_id__in=patients)

            if not treatments.exists():
                self.stdout.write(self.style.WARNING(f"No treatments found for patients associated with user ID {user_id}."))
                return

            # Update the doctor for all selected treatments
            updated_count = treatments.update(doctor=doctor)

            self.stdout.write(self.style.SUCCESS(
                f"Successfully assigned Doctor (ID: {doctor_id}) to {updated_count} treatments associated with User (ID: {user_id})."
            ))

        except Doctor.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Doctor with ID {doctor_id} does not exist."))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with ID {user_id} does not exist."))
