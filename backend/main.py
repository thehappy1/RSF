from fastapi import FastAPI, APIRouter, HTTPException
import pandas as pd
from pydantic import BaseModel
from models import XGBoostModel  # Stellen Sie sicher, dass models.py existiert und XGBoostModel definiert ist
from data import DataUtils  # Stellen Sie sicher, dass data.py existiert und DataUtils definiert ist
from core.config import DATA_PATH, FEATURE_LIST  # Stellen Sie sicher, dass core/config.py existiert und diese Variablen definiert sind
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()  # Hier definieren wir die FastAPI-Anwendung
router = APIRouter()

class Data(BaseModel):
    store_id: int
    forecast_weeks: int = 6

# Initialisierung des Modells und Laden der Daten beim Start der Anwendung
try:
    model = XGBoostModel()
    df = DataUtils.load_data('/app/data/final_df_w_fe.csv')
except Exception as e:
    logger.error(f"Fehler beim Initialisieren des Modells oder Laden der Daten: {str(e)}")
    model = None
    df = None

@router.post("/forecast")
async def create_forecast(data: Data):
    try:
        if model is None or df is None:
            raise HTTPException(status_code=500, detail="Modell oder Daten konnten nicht geladen werden")

        X_train, y_train, train, X_test, y_test, test = DataUtils.create_holdout_set(
            df, store_id=data.store_id, feature_list=FEATURE_LIST, anzahl_wochen=data.forecast_weeks, get_full_data=True
        )

        forecast = model.get_predictions_for_store(
            input_data=X_test, store_id=data.store_id, future_steps=data.forecast_weeks
        )

        train_json = train.to_json(orient="records")
        test_json = test.to_json(orient="records")
        
        return {
            "forecast": forecast.tolist() if hasattr(forecast, 'tolist') else forecast,
            "dates": test['Date'].tolist() if hasattr(test, 'tolist') else list(test['Date']),
            "test": test_json,
            "train": train_json
        }
    
    except Exception as e:
        logger.error(f"Fehler beim Ausführen der Vorhersagen: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fehler beim Ausführen der Vorhersagen: {str(e)}")

# Routen registrieren
app.include_router(router)