import xgboost as xgb
import pandas as pd
import numpy as np
import os
import sys

# Add the backend directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import MODEL_PATH  

class XGBoostModel():
    def __init__(self, model_path="/app/models/xgboost_final.json"):
        self.xgb_model = self.load_xgb_model(model_path)

    def load_xgb_model(self, MODEL_PATH):
        '''
        Load XGBoost model
        '''
        try:
            xgb_model = xgb.Booster()
            xgb_model.load_model(MODEL_PATH)
            print("Model erfolgreich geladen")
        except Exception as e:
            print('Model Loading fehlgeschlagen! Fehler', e)
            xgb_model = xgb.Booster()

        return xgb_model

    def get_predictions_for_store(self, input_data, store_id, future_steps):
        # Select Test Data for store_id
        # Das hier sollte sogar noch ein Schritt vorher erfolgen

        dtest_store = xgb.DMatrix(input_data, enable_categorical=True)

        # Get prediction
        predictions_xgb = self.xgb_model.predict(dtest_store)

        # Transform 
        predictions_xgb = np.expm1(predictions_xgb)

        return predictions_xgb