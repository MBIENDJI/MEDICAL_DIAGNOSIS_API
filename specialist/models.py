# specialist/models.py

import json
from django.db import models
from cryptography.fernet import Fernet

# ===== Clé Fernet pour le chiffrement =====
FERNET_KEY = b'kWRqyL7e4dDNvf-bo6zHlAi-yRacsLC0U8olJeS-OY4='
fernet = Fernet(FERNET_KEY)

# ===== Modèle pour stocker un diagnostic préliminaire =====
class PreliminaryDiagnosis(models.Model):
    patient_name = models.CharField(max_length=255, blank=True, null=True)
    symptoms = models.TextField()  # JSON encrypté
    predictions = models.TextField()  # JSON encrypté, ex: {"disease": "Malaria", "confidence": 0.85}
    created_at = models.DateTimeField(auto_now_add=True)

    def set_symptoms(self, symptoms_dict):
        """Chiffre et stocke les symptômes."""
        json_data = json.dumps(symptoms_dict)
        self.symptoms = fernet.encrypt(json_data.encode()).decode()

    def get_symptoms(self):
        """Déchiffre les symptômes."""
        if not self.symptoms:
            return {}
        decrypted = fernet.decrypt(self.symptoms.encode()).decode()
        return json.loads(decrypted)

    def set_predictions(self, predictions_dict):
        """Chiffre et stocke les prédictions."""
        json_data = json.dumps(predictions_dict)
        self.predictions = fernet.encrypt(json_data.encode()).decode()

    def get_predictions(self):
        """Déchiffre les prédictions."""
        if not self.predictions:
            return {}
        decrypted = fernet.decrypt(self.predictions.encode()).decode()
        return json.loads(decrypted)

    def __str__(self):
        return f"PreliminaryDiagnosis {self.id} - {self.patient_name or 'Unknown'}"


# ===== Modèle pour stocker les spécialistes prédits =====
class SpecialistRecommendation(models.Model):
    diagnosis = models.ForeignKey(PreliminaryDiagnosis, on_delete=models.CASCADE, related_name="specialists")
    specialist_type = models.CharField(max_length=255)  # ex: "Neurologist"
    priority = models.CharField(max_length=50, default="Moyenne")  # ex: "Haute", "Moyenne", "Basse"

    def __str__(self):
        return f"{self.specialist_type} ({self.priority}) for Diagnosis {self.diagnosis.id}"


# ===== Modèle pour les évaluations de risque d'un patient =====
class RiskAssessment(models.Model):
    patient_name = models.CharField(max_length=255, blank=True, null=True)
    data = models.TextField()  # JSON encrypté contenant paramètres du patient
    risk_factors = models.TextField()  # JSON encrypté {"diabetes": "Élevé", "hypertension": "Faible"}
    recommendations = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_data(self, data_dict):
        json_data = json.dumps(data_dict)
        self.data = fernet.encrypt(json_data.encode()).decode()

    def get_data(self):
        if not self.data:
            return {}
        decrypted = fernet.decrypt(self.data.encode()).decode()
        return json.loads(decrypted)

    def set_risk_factors(self, risk_dict):
        json_data = json.dumps(risk_dict)
        self.risk_factors = fernet.encrypt(json_data.encode()).decode()

    def get_risk_factors(self):
        if not self.risk_factors:
            return {}
        decrypted = fernet.decrypt(self.risk_factors.encode()).decode()
        return json.loads(decrypted)

    def __str__(self):
        return f"RiskAssessment {self.id} - {self.patient_name or 'Unknown'}"
