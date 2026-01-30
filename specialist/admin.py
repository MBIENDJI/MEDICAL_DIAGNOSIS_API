from django.contrib import admin
from .models import PreliminaryDiagnosis, SpecialistRecommendation, RiskAssessment

@admin.register(PreliminaryDiagnosis)
class PreliminaryDiagnosisAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'created_at')

@admin.register(SpecialistRecommendation)
class SpecialistRecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'diagnosis', 'specialist_type', 'priority')

@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'created_at')
