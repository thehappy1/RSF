import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import requests
import io

# Set page config
st.set_page_config(page_title="Store Sales Demand Forecast", layout="wide")

# Title
st.title("Store Sales Demand Forecasting")

# Sidebar
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    
    # Display the raw data
    st.subheader("Raw Data")
    st.write(data.head())
    
    # Create future dataframe for predictions
    future_period = st.sidebar.slider("Forecast period (days)", min_value=1, max_value=365, value=30)
    
    # Make API request to backend
    files = {'file': uploaded_file.getvalue()}
    response = requests.post("http://backend:8000/forecast", files=files, data={'forecast_days': future_period})
    forecast_data = response.json()
    
    # Plot the forecast
    st.subheader("Sales Forecast")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['date'], y=data['sales'], mode='lines', name='Historical Data'))
    fig.add_trace(go.Scatter(x=[d['ds'] for d in forecast_data['forecast']], 
                             y=[d['yhat'] for d in forecast_data['forecast']], 
                             mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=[d['ds'] for d in forecast_data['forecast']], 
                             y=[d['yhat_upper'] for d in forecast_data['forecast']], 
                             fill=None, mode='lines', line_color='rgba(0,100,80,0.2)', name='Upper Bound'))
    fig.add_trace(go.Scatter(x=[d['ds'] for d in forecast_data['forecast']], 
                             y=[d['yhat_lower'] for d in forecast_data['forecast']], 
                             fill='tonexty', mode='lines', line_color='rgba(0,100,80,0.2)', name='Lower Bound'))
    st.plotly_chart(fig)
    
    # Display forecast components
    st.subheader("Forecast Components")
    components_fig = go.Figure()
    components_fig.add_trace(go.Scatter(x=[p[0] for p in forecast_data['components']['trend']], 
                                        y=[p[1] for p in forecast_data['components']['trend']], 
                                        mode='lines', name='Trend'))
    components_fig.add_trace(go.Scatter(x=[p[0] for p in forecast_data['components']['yearly']], 
                                        y=[p[1] for p in forecast_data['components']['yearly']], 
                                        mode='lines', name='Yearly'))
    components_fig.add_trace(go.Scatter(x=[p[0] for p in forecast_data['components']['weekly']], 
                                        y=[p[1] for p in forecast_data['components']['weekly']], 
                                        mode='lines', name='Weekly'))
    st.plotly_chart(components_fig)
    
    # Show forecast data
    st.subheader("Forecast Data")
    st.write(pd.DataFrame(forecast_data['forecast']).tail())

else:
    st.write("Please upload a CSV file to begin forecasting.")

# Instructions
st.sidebar.markdown("""
## Instructions
1. Upload a CSV file containing sales data.
2. The CSV should have 'date' and 'sales' columns.
3. Adjust the forecast period using the slider.
4. View the forecast plot and components.
""")
    