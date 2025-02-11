# monitoring/management/commands/populate_treatment_days.py

from django.core.management.base import BaseCommand
from django.db.models import Max
from datetime import timedelta, date
from monitoring.models import Treatment

class Command(BaseCommand):
    help = 'Populate missing dates for day0, day3, and day7 fields and mark arrived as True'

    def handle(self, *args, **options):
        # Step 1: Identify the latest date in any of the day fields in 2024
        latest_date = Treatment.objects.aggregate(
            max_day0=Max('day0'),
            max_day3=Max('day3'),
            max_day7=Max('day7')
        )
        
        # Find the latest non-null date in 2024
        starting_date = max(
            date for date in [
                latest_date['max_day0'],
                latest_date['max_day3'],
                latest_date['max_day7']
            ] if date and date.year == 2024
        ) if any(date for date in latest_date.values()) else date(2024, 1, 1)

        # Step 2: Filter treatments with missing day0, day3, or day7
        treatments_to_update = Treatment.objects.filter(
            day0__isnull=True
        ) | Treatment.objects.filter(
            day3__isnull=True
        ) | Treatment.objects.filter(
            day7__isnull=True
        )

        # Step 3: Populate missing dates and set all arrived fields to True
        for treatment in treatments_to_update:
            if not treatment.day0:
                treatment.day0 = starting_date
            if not treatment.day3:
                treatment.day3 = treatment.day0 + timedelta(days=3)
            if not treatment.day7:
                treatment.day7 = treatment.day0 + timedelta(days=7)

            # Set all arrived fields to True
            treatment.day0_arrived = True
            treatment.day3_arrived = True
            treatment.day7_arrived = True

            # Save updated treatment
            treatment.save()

            # Update the starting date for the next treatment
            starting_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS("Successfully populated missing dates and set arrived to True for day0, day3, and day7."))
