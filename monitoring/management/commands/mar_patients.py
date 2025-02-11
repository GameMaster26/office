from django.core.management.base import BaseCommand
from faker import Faker
import random
from monitoring.models import Patient, Municipality, Barangay, History, Treatment, User, Doctor
from django.contrib.auth.models import User as AuthUser
from datetime import timedelta, date, datetime
from nameparser import HumanName

class Command(BaseCommand):
    help = 'Generates 10 random patients with history and treatment records for User 2'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Get the specific User with id=2
        user = User.objects.get(id=3)

        doctor = Doctor.objects.get(id=4)

        # Get all existing Municipality instances
        municipalities = Municipality.objects.all()

        # Set default municipality to the one with ID 1
        default_municipality = Municipality.objects.get(muni_id=9)

        # Get all Barangays related to the selected Municipality
        barangays = default_municipality.barangays.all()
        if not barangays:
            print(f"No barangays found for {default_municipality.muni_name}")
            return

        # Define possible bite sites
        bite_sites = [
            'right arm', 'left arm', 'right leg', 'left leg', 'right hand',
            'left hand', 'back', 'shoulder', 'abdomen', 'thigh', 'calf', 'ankle',
            'right lower leg','right infrascapular','right index finger',
            '1st digit right foot','right posterior leg','right wrist','left wrist',
        ]

        def determine_sex(first_name):
            """Determine sex based on first name."""
            name = HumanName(first_name)
            if name.first in fake.first_name_male():
                return 'male'
            elif name.first in fake.first_name_female():
                return 'female'
            return 'unknown'  # Return unknown if gender cannot be determined

        def generate_registration_no(user):
            current_year = date.today().year

            # Find the latest registration number for the current year for the specific user
            last_history = History.objects.filter(
                patient_id__user=user,  # Filter by the specific user
                registration_no__startswith=f'{current_year}-'
            ).order_by('registration_no').last()

            if last_history:
                last_reg_no = last_history.registration_no
                last_reg_num = int(last_reg_no.split('-')[-1])
                new_reg_num = last_reg_num + 1
            else:
                new_reg_num = 1  # If no history found, start from 1 for this user

            new_registration_no = f'{current_year}-{new_reg_num:05d}'
            return new_registration_no
        


        def create_patients_with_history_and_treatment(n=10):
            # Get the last registered date (latest date) for this user in the first quarter of 2024
            latest_history = History.objects.filter(
                patient_id__user=user,  # Filter by the specific user
                date_registered__gte=date(2024, 10, 1),
                date_registered__lte=date(2024, 12,31)
            ).order_by('-date_registered').first()

            # If no records are found in the first quarter, start from Jan 1st
            if latest_history:
                start_date = latest_history.date_registered + timedelta(days=3)  # Start from the next day
            else:
                start_date = date(2024, 10, 1)  # If no records, start from Jan 1st



            # Generate patients with sequential dates in the first quarter
            for i in range(n):
                # Randomly select Barangay within the same Municipality
                barangay = random.choice(barangays)

                # Generate random patient details using Faker
                first_name = fake.first_name()
                middle_name = fake.last_name()
                last_name = fake.last_name()
                birthday = fake.date_of_birth(minimum_age=3, maximum_age=70)
                contact_number = '09' + ''.join([str(random.randint(0, 9)) for _ in range(9)])
                sex = determine_sex(first_name)

                # Create and save the Patient instance
                patient = Patient(
                    user=user,
                    doctor=doctor,
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    muni_id=default_municipality,
                    brgy_id=barangay,
                    birthday=birthday,
                    sex=random.choice(['male', 'female']),
                    contactNumber=contact_number
                )
                patient.save()
                print(f"Patient {first_name} {last_name} created in {barangay.brgy_name}, {default_municipality.muni_name}!")

                # Generate the correct registration number
                registration_no = generate_registration_no(user)

                # Generate date_registered for the patient, ensuring it is sequential
                date_registered = start_date + timedelta(days=i)  # Generate sequential dates

                # Ensure date_registered does not go beyond March 31st
                if date_registered > date(2024, 12,31):
                    date_registered = date(2024, 12,31)   # Cap it to March 31st if it exceeds

                # Create date of exposure - ensure it is before date_registered
                date_of_exposure = date_registered - timedelta(days=random.randint(1, 30))

                # Create and save a History instance for the patient
                history = History(
                    patient_id=patient,
                    registration_no=registration_no,
                    muni_id=default_municipality,
                    brgy_id=barangay,
                    date_registered=date_registered,
                    date_of_exposure=date_of_exposure,
                    category_of_exposure='II',  # Always set to "II"
                    source_of_exposure=random.choice(['Dog', 'Cat']),
                    exposure_type=random.choice(['Bite', 'Non-Bite']),
                    bite_site=random.choice(bite_sites),  # Random body part
                    provoked_status=random.choice(['Provoked', 'Unprovoked']),
                    immunization_status=random.choice(['Immunized', 'Unimmunized']),
                    status_of_animal=random.choice(['Alive', 'Dead', 'Killed', 'Lost']),
                    confinement_status=random.choice(['Stray', 'Leashed/Caged']),
                    washing_hands=random.choice(['Yes', 'No']),
                    latitude=0.0,  # Placeholder
                    longitude=0.0,  # Placeholder
                    geom=None  # Placeholder
                )
                history.save()
                print(f"History created for {first_name} {last_name}!")

                # Day 0, Day 3, Day 7 based on date_registered
                day0 = date_registered
                day3 = day0 + timedelta(days=3)
                day7 = day3 + timedelta(days=4)

                # Create and save a Treatment instance for the patient
                treatment = Treatment(
                    patient_id=patient,
                    vaccine_generic_name=random.choice(['PCECCV', 'PVRV']),
                    vaccine_brand_name=random.choice(['Verorab', 'Speeda', 'Vaxirab', 'Abhayrab']),
                    vaccine_route='intradermal',  # Always set to "intradermal"
                    tcv_given=day0,  # TCV on the same day as date_registered
                    day0=day0,  # Day 0 same as date_registered
                    day3=day3,  # Day 3 is 3 days after Day 0
                    day7=day7,  # Day 7 is 4 days after Day 3
                )
                treatment.save()
                print(f"Treatment created for {first_name} {last_name}!")

        # Generate 10 patients with history and treatment records, starting from the latest date_registered
        create_patients_with_history_and_treatment(3)
        self.stdout.write(self.style.SUCCESS('Successfully generated 10 patients with history and treatment records for User 2'))
