from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

router = APIRouter()

class Data(BaseModel):
    store_id: int
    forecast_horizon: int

logger = logging.getLogger(__name__)

@router.post("/predict")
def predict(input_data: Data):
    """
    Generate sales predictions for a specified store and forecast horizon.

    Args:
        input_data (Data): Input data containing the store ID and forecast horizon.

    Returns:
        dict: A dictionary containing store data, predictions, and dates.

    Raises:
        HTTPException: If an error occurs during the prediction process.
    """
    try:
        store_data, predictions, dates = get_predictions(model, input_data.store_id, input_data.forecast_horizon)
        logger.info(f"Vorhersage für Store {input_data.store_id} mit Horizont {input_data.forecast_horizon}: {predictions}")
        return {"store_data": store_data, "predictions": predictions, "dates": dates}
    except Exception as e:
        logger.error(f"Fehler beim Ausführen der Vorhersagen: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
