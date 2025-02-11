import random
from django.core.management.base import BaseCommand
from django.db import transaction
from monitoring.models import History  # Adjust your app name accordingly

class Command(BaseCommand):
    help = 'Update all History instances with a random bite site'

    def handle(self, *args, **options):
        bite_site_choices = [
            'Front of Head', 'Back of Head', 'Face', 'Jaw', 'Mouth', 
            'Eye', 'Cheek', 'Forehead', 'Temple', 'Behind Ear',
            'Front of Neck', 'Back of Neck', 'Shoulder (Left)', 
            'Shoulder (Right)', 'Upper Arm (Left)', 'Upper Arm (Right)', 
            'Elbow (Left)', 'Elbow (Right)', 'Forearm (Left)', 
            'Forearm (Right)', 'Wrist (Left)', 'Wrist (Right)', 
            'Palm (Left)', 'Palm (Right)', 'Back of Hand (Left)', 
            'Back of Hand (Right)', 'Thumb (Left)', 'Thumb (Right)', 
            'Index Finger (Left)', 'Index Finger (Right)', 
            'Middle Finger (Left)', 'Middle Finger (Right)', 
            'Ring Finger (Left)', 'Ring Finger (Right)', 
            'Little Finger (Left)', 'Little Finger (Right)',
            'Chest (Front)', 'Chest (Side)', 'Abdomen (Front)', 
            'Lower Back', 'Hip (Left)', 'Hip (Right)', 
            'Thigh (Left, Front)', 'Thigh (Left, Back)', 
            'Thigh (Right, Front)', 'Thigh (Right, Back)', 
            'Knee (Left, Front)', 'Knee (Left, Back)', 
            'Knee (Right, Front)', 'Knee (Right, Back)', 
            'Calf (Left)', 'Calf (Right)', 'Leg (Left)', 
            'Leg (Right)', 'Leg Lower(Left)', 'Leg Lower(Right)', 
            'Leg Upper(Left)', 'Leg Upper(Right)', 'Leg Anterior(Left)', 
            'Leg Anterior(Right)', 'Leg Posterior(Left)', 
            'Leg Posterior(Right)', 'Ankle (Left)', 'Ankle (Right)', 
            'Foot (Left)', 'Foot (Right)', 'Toes (Left)', 
            'Toes (Right)', 'Ball of Foot (Left)', 
            'Ball of Foot (Right)', 'Heel (Left)', 'Heel (Right)',
        ]

        histories = History.objects.all()
        updated_histories = []  # List to hold updated History instances

        with transaction.atomic():  # Start a transaction
            for history in histories:
                history.bite_site = random.choice(bite_site_choices)
                updated_histories.append(history)  # Collect the updated instances
            
            # Bulk update the instances
            History.objects.bulk_update(updated_histories, ['bite_site'])

        self.stdout.write(self.style.SUCCESS('Successfully updated bite sites for all histories.'))
