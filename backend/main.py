from fastapi import FastAPI, UploadFile, File
from prophet import Prophet
import pandas as pd
import io
import json

app = FastAPI()

@app.post("/forecast")
async def create_forecast(file: UploadFile = File(...), forecast_days: int = 30):
    content = await file.read()
    data = pd.read_csv(io.StringIO(content.decode('utf-8')))
    
    # Prepare data for Prophet
    df = data[['date', 'sales']].rename(columns={'date': 'ds', 'sales': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])
    
    # Create and fit the model
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(df)
    
    # Create future dataframe for predictions
    future = model.make_future_dataframe(periods=forecast_days)
    
    # Make predictions
    forecast = model.predict(future)
    
    # Prepare the response
    forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records')
    components = model.plot_components(forecast)
    components_data = {
        'trend': components.gca().lines[0].get_xydata().tolist(),
        'yearly': components.gca().lines[1].get_xydata().tolist(),
        'weekly': components.gca().lines[2].get_xydata().tolist()
    }
    
    return {
        "forecast": forecast_data,
        "components": components_data
    }
