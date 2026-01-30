# specialist/tasks.py

from django.utils import timezone
from .models import PreliminaryDiagnosis  # Utilise ton modèle actuel
import datetime

def delete_old_preliminary_diagnoses(hours=1):
    """
    Supprime les PreliminaryDiagnosis vieux de plus de 'hours' heures.
    """
    cutoff_time = timezone.now() - datetime.timedelta(hours=hours)
    deleted_count, _ = PreliminaryDiagnosis.objects.filter(created_at__lt=cutoff_time).delete()
    print(f"{deleted_count} old preliminary diagnoses deleted.")
