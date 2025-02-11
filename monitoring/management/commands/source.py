import random
from django.core.management.base import BaseCommand
from monitoring.models import History  # Adjust your app name accordingly

class Command(BaseCommand):
    help = 'Update empty source_of_exposure fields in History instances with a random source of exposure'

    def handle(self, *args, **options):
        # Define source of exposure choices, excluding 'Dog' and 'Cat'
        source_of_exposure_choices = [
            'Monkey', 'Human', 'Cow',
             'Pig'
        ]

        # Filter for History instances where source_of_exposure is empty
        histories = History.objects.filter(source_of_exposure__isnull=True) | History.objects.filter(source_of_exposure='')
        
        if not histories.exists():
            self.stdout.write(self.style.WARNING('No empty source_of_exposure fields found.'))
            return

        for history in histories:
            # Select a random source of exposure from choices
            history.source_of_exposure = random.choice(source_of_exposure_choices)
            history.save()  # Save the updated instance
            self.stdout.write(self.style.SUCCESS(f'Updated source of exposure for history ID {history.history_id} to {history.source_of_exposure}'))

        self.stdout.write(self.style.SUCCESS('Successfully updated source of exposure for all histories with empty fields.'))
