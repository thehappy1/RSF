from fastapi import APIRouter, HTTPException
import pandas as pd
from pydantic import BaseModel
from models import XGBoostModel
from data import DataUtils
from core.config import DATA_PATH, FEATURE_LIST
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
class Data(BaseModel):
    store_id: int
    forecast_horizon: int = 7

model = XGBoostModel()
df = DataUtils.load_data(DATA_PATH)

@router.post("/forecast")
async def create_forecast(store_id, forecast_days: int = 14):
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="Modell konnte nicht geladen werden")
        
        X_train, y_train, X_test, y_test, train_dates, test_dates = DataUtils.create_holdout_set(df, store_id=store_id, feature_list=FEATURE_LIST, anzahl_wochen=6, get_dates=True)
        forecast = model.get_predictions_for_store(input_data=X_test, store_id=store_id, future_steps=forecast_days)

        return {
            "forecast": forecast,
            "dates": test_dates
        }
    except Exception as e:
        logger.error(f"Fehler beim Ausführen der Vorhersagen: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fehler beim Ausführen der Vorhersagen: {str(e)}")