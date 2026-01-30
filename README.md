


 API de Diagnostic de Santé Préliminaire
Description du projet
Cette API REST permet d’orienter un patient vers un ou plusieurs spécialistes médicaux à partir de ses symptômes et de données biométriques, en utilisant un modèle de Machine Learning multi-label.
Le projet met un accent particulier sur :
•	La confidentialité des données de santé
•	La classification multi-label (plusieurs spécialistes possibles)
•	La conformité RGPD (anonymisation, durée de conservation)
⚠️ Disclaimer (présent dans chaque réponse API)
Ceci n’est pas un diagnostic médical. Consultez un professionnel de santé.
________________________________________
 Architecture du projet
Recommendation_by_specialists/
│
├── health_diagnosis_api/
│   ├── settings.py
│   ├── urls.py
│
├── specialist/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tasks.py
│   ├── ml_model/
│   │   └── MLabelRF_specialist.joblib
│
├── db.sqlite3
├── manage.py
└── README.md
________________________________________
 Technologies utilisées
•	Python 3
•	Django
•	Django REST Framework
•	drf-spectacular (schéma OpenAPI)
•	scikit-learn
o	MultiOutputClassifier
o	RandomForestClassifier
•	Dataset Kaggle : Disease Symptom Prediction
•	Postman (tests API)
•	Chiffrement Fernet (cryptography)
________________________________________
 Sécurité & RGPD
•	Les données sensibles (symptômes, facteurs de risque) sont :
o	chiffrées avec Fernet
o	stockées sous forme anonymisée
•	Les diagnostics préliminaires sont :
o	supprimés automatiquement après un délai (via tasks.py)
•	Aucune donnée médicale n’est conservée à long terme
________________________________________
 Installation du projet
1️ Cloner le projet
git clone <url-du-repo>
cd Recommendation_by_specialists
2️ Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate   # Windows
3️ Installer les dépendances
pip install django djangorestframework drf-spectacular scikit-learn cryptography joblib
4️  Appliquer les migrations
python manage.py makemigrations
python manage.py migrate
5️ Lancer le serveur
python manage.py runserver
Serveur disponible sur :
 http://127.0.0.1:8000/
________________________________________
 Endpoints de l’API (workflow complet)
 1. Recherche de symptômes (autocomplétion)
GET /api/symptoms/search/?q=<mot-clé>
Exemple
GET /api/symptoms/search/?q=hea
Réponse
[
  "headache",
  "hearing loss"
]
________________________________________
2. Diagnostic préliminaire (génération de l’ID)
POST /api/diagnoses/preliminary/
Body
{
  "symptoms": ["headache", "nausea", "blurred vision"]
}
Réponse
{
  "id": 5,
  "preliminary_diagnoses": [
    {
      "disease": "Migraine",
      "confidence": 0.82
    }
  ],
  "disclaimer": "Ceci n’est pas un diagnostic médical. Consultez un professionnel."
}
 L’id généré est utilisé dans les étapes suivantes.
________________________________________
3. Spécialistes recommandés (classification multi-label)
GET /api/diagnoses/{id}/specialists/
Exemple
GET /api/diagnoses/5/specialists/
Réponse
{
  "specialists": [
    {
      "type": "Neurologist",
      "priority": "High"
    },
    {
      "type": "General Practitioner",
      "priority": "High"
    }
  ],
  "disclaimer": "Ceci n’est pas un diagnostic médical. Consultez un professionnel."
}
 Le modèle ML peut prédire plusieurs spécialistes simultanément.
________________________________________
 4. Évaluation des risques patient
POST /api/patients/{id}/risk-assessment/
Body
{
  "blood_pressure": "150/95",
  "bmi": 29.5,
  "family_history": true
}
Réponse
{
  "risk_factors": {
    "diabetes": "Low",
    "hypertension": "High"
  },
  "recommendations": "Réduire le sel et surveiller la pression artérielle.",
  "disclaimer": "Ceci n’est pas un diagnostic médical. Consultez un professionnel."
}
________________________________________
Machine Learning
•	Type : Classification multi-label
•	Modèle :
•	MultiOutputClassifier(RandomForestClassifier)
•	Dataset : Kaggle – Disease Symptom Prediction
•	Sorties possibles :
o	Neurologist
o	Cardiologist
o	General Practitioner
o	Dermatologist
________________________________________
 Tests API
•	Les tests ont été réalisés avec Postman
•	Les captures d’écran et illustrations sont disponibles dans :
 Project_Description.doc
Ce document montre :
•	Le chiffrement des données avant modification en une autre façon
•	Les appels Postman
•	Le déroulement complet du workflow
________________________________________
 Objectifs du projet respectés
 4 endpoints minimum
Multi-label ML
Chiffrement des données
RGPD (anonymisation + durée de conservation)
Disclaimer médical Dataset Kaggle utilisé
________________________________________
 Auteur
Mbiendji Sébastien
Projet académique – API Django REST & Machine Learning

Les démarches se trouve dans le fichier word joint


