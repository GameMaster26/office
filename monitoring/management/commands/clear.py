from django.core.management.base import BaseCommand
from monitoring.models import Patient, History, Treatment

class Command(BaseCommand):
    help = 'Clears all generated patient data including history and treatment records'

    def handle(self, *args, **kwargs):
        # Delete all Treatment records
        Treatment.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All Treatment records have been deleted.'))

        # Delete all History records
        History.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All History records have been deleted.'))

        # Delete all Patient records
        Patient.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All Patient records have been deleted.'))
