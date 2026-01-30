from django.urls import path
from .views import (
    SymptomSearchView,
    PreliminaryDiagnosisView,
    SpecialistsView,
    RiskAssessmentView
)

urlpatterns = [
    path("symptoms/search/", SymptomSearchView.as_view(), name="symptom-search"),

    # STEP (a)
    path(
        "diagnoses/preliminary/",
        PreliminaryDiagnosisView.as_view(),
        name="preliminary-diagnosis"
    ),

    # STEP (b) ⚠️ int et PAS uuid
    path(
        "diagnoses/<int:diag_id>/specialists/",
        SpecialistsView.as_view(),
        name="diagnosis-specialists"
    ),

    # STEP (c)
    path(
        "patients/<int:patient_id>/risk-assessment/",
        RiskAssessmentView.as_view(),
        name="risk-assessment"
    ),
]
