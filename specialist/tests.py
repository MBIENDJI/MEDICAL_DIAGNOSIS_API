from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import PreliminaryDiagnosis, SpecialistRecommendation, RiskAssessment


class SymptomSearchTests(APITestCase):

    def test_symptom_search(self):
        url = reverse("symptom-search")
        response = self.client.get(url, {"q": "hea"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("headache", response.data)


class PreliminaryDiagnosisTests(APITestCase):

    def test_create_preliminary_diagnosis(self):
        url = reverse("preliminary-diagnosis")
        payload = {
            "symptoms": ["headache", "nausea", "fatigue"]
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("preliminary_diagnoses", response.data)

        # Vérifier que l'objet est bien créé
        self.assertEqual(PreliminaryDiagnosis.objects.count(), 1)

        diag = PreliminaryDiagnosis.objects.first()
        self.assertEqual(diag.get_symptoms(), payload["symptoms"])


class SpecialistRecommendationTests(APITestCase):

    def setUp(self):
        self.diag = PreliminaryDiagnosis.objects.create()
        self.diag.set_symptoms(["headache", "blurred vision"])
        self.diag.set_predictions(
            [{"disease": "Migraine", "confidence": 0.82}]
        )
        self.diag.save()

    def test_get_specialists_for_diagnosis(self):
        url = reverse(
            "diagnosis-specialists",
            kwargs={"diag_id": self.diag.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("specialists", response.data)
        self.assertTrue(len(response.data["specialists"]) > 0)

        # Vérifier l'enregistrement en base
        self.assertTrue(
            SpecialistRecommendation.objects.filter(diagnosis=self.diag).exists()
        )


class RiskAssessmentTests(APITestCase):

    def test_create_risk_assessment(self):
        url = reverse(
            "risk-assessment",
            kwargs={"patient_id": 1}
        )

        payload = {
            "blood_pressure": "140/90",
            "bmi": 29.5,
            "family_history": True
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("risk_factors", response.data)
        self.assertIn("recommendations", response.data)

        self.assertEqual(RiskAssessment.objects.count(), 1)

        risk = RiskAssessment.objects.first()
        self.assertEqual(risk.get_data(), payload)
