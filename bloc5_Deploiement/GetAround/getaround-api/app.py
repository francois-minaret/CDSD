from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from typing import Literal
import pandas as pd
import traceback
import boto3
import os
import tempfile

app = FastAPI(title="GetAround - API de prédiction de prix",
    description="""
### 🎯 Description  <br>
Cette API prédit le prix de location d'une voiture à la journée.<br>
<br>
Il y a 3 types de variables : <br>
    - Les sélectives <br>
        - modele: ['Citroën','Peugeot','PGO','Renault','Audi','BMW','Ford','Mercedes','Opel','Volkswagen','Porsche','KIAMotors','AlfaRomeo','Ferrari','Fiat','Lamborghini','Maserati','Lexus','Honda','Mazda','Mitsubishi','Nissan','SEAT','Subaru','Suzuki','Toyota','Yamaha']<br>
        - essence: ['diesel', 'essence', 'Hybride', 'Eletrique']<br>
        - Couleur: ['Noir','Blanc','Rouge','Argent','Gris','Bleu','Orange','Beige','Marron','Vert']<br>
        - Type: ['Cabriolet','Coupé','Break','Compacte','Berline','Sous-compacte','SUV','Van']<br>
    - les numériques :<br>
        - kilometrage<br>
        - puissance: float<br>
    - les chaines de caractères (Oui/Non) :<br>
        - parking<br>
        - GPS<br>
        - Climatisation<br>
        - Boite_auto<br>
        - Systeme_GetAround<br>
        - Regulateur<br>
        - Pneus_hiver<br>
<br>
Exemple :  <br>
```json
{
  "modele": "Ford",
  "kilometrage": 29464,
  "puissance": 160,
  "essence": "diesel",
  "couleur": "Blanc",
  "type": "Compacte",
  "parking": "Non",
  "GPS": "Non",
  "Climatisation": "Non",
  "Boite_auto": "Non",
  "Systeme_GetAround": "Non",
  "Regulateur": "Non",
  "Pneus_hiver": "Non"
}
""")

# Chargement du modèle
# Path_XGB = "XGBoost_API.pkl"
# model = joblib.load(Path_XGB)
BUCKET_NAME = "getaround-fmi"
OBJECT_KEY = "modele/XGBoost_API.pkl"
def load_model_from_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION")
    )

    # Télécharger le fichier dans un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        s3.download_fileobj(BUCKET_NAME, OBJECT_KEY, tmp)
        tmp_path = tmp.name

    # Charger le modèle
    model = joblib.load(tmp_path)
    return model

# Chargement une seule fois au démarrage
model = load_model_from_s3()


print(model)

#Variables d'entrée
class GetAround_Variables(BaseModel):
    modele: Literal['Citroën','Peugeot','PGO','Renault','Audi','BMW','Ford','Mercedes','Opel','Volkswagen','Porsche','KIAMotors','AlfaRomeo','Ferrari','Fiat','Lamborghini','Maserati','Lexus','Honda','Mazda','Mitsubishi','Nissan','SEAT','Subaru','Suzuki','Toyota','Yamaha']
    kilometrage: float
    puissance: float
    essence: Literal['diesel', 'essence', 'Hybride', 'Eletrique']
    couleur: Literal['Noir','Blanc','Rouge','Argent','Gris','Bleu','Orange','Beige','Marron','Vert']
    type: Literal['Cabriolet','Coupé','Break','Compacte','Berline','Sous-compacte','SUV','Van']
    parking: Literal['Oui','Non']
    GPS: Literal['Oui','Non']
    Climatisation: Literal['Oui','Non']
    Boite_auto: Literal['Oui','Non']
    Systeme_GetAround: Literal['Oui','Non']
    Regulateur: Literal['Oui','Non']
    Pneus_hiver: Literal['Oui','Non']

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API GetAround pour la prédiction de prix de location"}

#Prédiciton
@app.post("/predict")
def predict(features: GetAround_Variables):
    try:
        input_df = pd.DataFrame([features.dict()])   

        # Prédiction
        prediction = model.predict(input_df)[0]
        
        return {
            "Prix à la location €/j prédit ": round(float(prediction), 2)
        }

    except Exception as e:
        print("ERREUR LORS DE LA PRÉDICTION :", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))