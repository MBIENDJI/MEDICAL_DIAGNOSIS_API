from rest_framework import serializers

class PreliminaryDiagnosisSerializer(serializers.Serializer):
    symptoms = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )
    duration = serializers.CharField(required=False)

class TemporaryDiagnosisSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    preliminary_diagnoses = serializers.ListField(
        child=serializers.DictField()  # {"disease": str, "confidence": float}
    )

class SpecialistSerializer(serializers.Serializer):
    type = serializers.CharField()
    priority = serializers.CharField()

class RiskAssessmentSerializer(serializers.Serializer):
    blood_pressure = serializers.CharField(required=False)
    bmi = serializers.FloatField(required=False)
    family_history = serializers.BooleanField(required=False)

class RiskAssessmentResultSerializer(serializers.Serializer):
    risk_factors = serializers.DictField()
    recommendations = serializers.CharField()


