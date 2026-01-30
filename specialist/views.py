# specialist/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from joblib import load
import json

from .models import PreliminaryDiagnosis, SpecialistRecommendation, RiskAssessment, fernet
from .serializers import (
    PreliminaryDiagnosisSerializer,
    SpecialistSerializer,
    RiskAssessmentSerializer
)

# ===== Charger le modèle multi-label =====
ml_specialist_model = load("specialist/ml_model/MLabelRF_specialist.joblib")
SPECIALIST_LABELS = ["Neurologist", "Cardiologist", "General Practitioner", "Dermatologist"]

# ===== Fonctions utilitaires =====

def predict_diseases(symptoms):
    """
    Placeholder pour prédire maladies + confiance.
    À remplacer par ton algorithme réel.
    """
    return [{"disease": "Migraine", "confidence": 0.82}]

def predict_specialists(symptoms):
    """
    Prédit plusieurs spécialistes à partir des symptômes.
    Utilise le modèle multi-label Joblib.
    """
    X_input = [" ".join(symptoms)]
    try:
        preds = ml_specialist_model.predict([X_input[0]])  # adapter selon ton modèle
    except Exception:
        # fallback si problème modèle
        preds = [[1, 0, 1, 0]]  # exemple
    result = []
    for idx, label in enumerate(SPECIALIST_LABELS):
        if preds[0][idx] == 1:
            result.append({"type": label, "priority": "High"})
    return result

def assess_risks(data):
    """
    Calcul du niveau de risque basé sur les facteurs du patient.
    """
    return {
        "risk_factors": {"diabetes": "Low", "hypertension": "High"},
        "recommendations": "Réduire consommation de sel"
    }

# ===== Endpoint (d) : Symptom Search =====
class SymptomSearchView(APIView):
    def get(self, request):
        q = request.GET.get("q", "").lower()
        all_symptoms = [
            "headache", "blurred vision", "fever", "cough",
            "nausea", "fatigue", "dizziness"
        ]
        suggestions = [s for s in all_symptoms if q in s.lower()]
        return Response(suggestions)

# ===== Endpoint (a) : Preliminary Diagnosis =====
class PreliminaryDiagnosisView(APIView):
    def post(self, request):
        serializer = PreliminaryDiagnosisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        symptoms = serializer.validated_data["symptoms"]

        predictions = predict_diseases(symptoms)

        diag = PreliminaryDiagnosis()
        diag.set_symptoms(symptoms)
        diag.set_predictions(predictions)
        diag.save()

        return Response({
            "id": diag.id,
            "preliminary_diagnoses": predictions
        }, status=status.HTTP_201_CREATED)

# ===== Endpoint (b) : Specialists for a Diagnosis =====
class SpecialistsView(APIView):
    def get(self, request, diag_id):
        diag = get_object_or_404(PreliminaryDiagnosis, id=diag_id)
        symptoms = diag.get_symptoms()

        specialists_list = predict_specialists(symptoms)

        # Enregistrer les spécialistes en base si pas déjà présents
        for spec in specialists_list:
            SpecialistRecommendation.objects.get_or_create(
                diagnosis=diag,
                specialist_type=spec["type"],
                defaults={"priority": spec["priority"]}
            )

        return Response({"specialists": specialists_list}, status=status.HTTP_200_OK)

# ===== Endpoint (c) : Risk Assessment =====
class RiskAssessmentView(APIView):
    def post(self, request, patient_id):
        serializer = RiskAssessmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        risk_result = assess_risks(serializer.validated_data)

        risk = RiskAssessment(
            patient_name=str(patient_id),
            recommendations=risk_result.get("recommendations")
        )
        risk.set_data(serializer.validated_data)
        risk.set_risk_factors(risk_result["risk_factors"])
        risk.save()

        return Response(risk_result, status=status.HTTP_201_CREATED)

