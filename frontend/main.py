import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import requests
import io

import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer

# Set page config
st.set_page_config(page_title="Store Sales Demand Forecast", layout="wide")

# Title
st.header("Rossmann Store Sales Demand Forecasting", divider='rainbow')

# Sidebar

# Filiale auswählen
store_list = np.arange(1,1116, dtype=int)
option_1 = st.sidebar.selectbox(
   "Bitte Filial-ID auswählen",
   (store_list),
   index=None,
   placeholder="Filiale auswählen...",
)

# Vorhersagelänge auswählen
length_list = np.arange(1,30, dtype=int)
option_2 = st.sidebar.selectbox(
   "Bitte Vorhersagelänge auswählen",
   (length_list),
   index=None,
   placeholder="Filiale auswählen...",
)

if st.sidebar.button("Berechne Vorhersage"):
    st.title(f'Dashboard für Filiale {option_1}')

    store_id = int(option_1)
    forecast_days = int(option_2)

    try:
        response = requests.post(
            "http://localhost:80/forecast",
            json={"store_id": store_id, "forecast_days": forecast_days}
        )

    except Exception as e:
        print(f'Anfordern der Vorhersage fehlgeschlagen. Fehler {e}')

    response_data = response.json()

    forecast_df = pd.DataFrame({
            "date": response_data['dates'],
            "forecast": response_data['forecast']
        })
    
    train_df = pd.read_json(response_data['train'], orient="records")
    test_df = pd.read_json(response_data['test'], orient="records")

    st.header("Key Performance Indicators 🚀")


    st.dataframe(train_df)

    fig = px.line(train_df, x="Date", y="Sales", color_discrete_sequence=["blue"], labels={'y': 'Verkaufszahlen'})
    fig.add_scatter(x=forecast_df['date'], y=forecast_df['forecast'], mode='lines', name='Vorhersage', line=dict(color='#41837E'))
    fig.add_scatter(x=test_df['Date'], y=test_df['Sales'], mode='lines', name='Echte Verkaufszahlen', line=dict(color='#236863'))
    fig.update_layout(title='Vorhersage der Verkaufszahlen', xaxis_title='Datum', yaxis_title='Verkaufszahlen in €')

    st.plotly_chart(fig, use_container_width=True)

    if st.button("Berechne Fehlermetrik"):
        st.text("Purrfect!")

st.sidebar.header("File Upload")
uploaded_file = st.sidebar.file_uploader("CSV einer eigenen Filiale hochladen...", type="csv")

# Instructions
st.sidebar.markdown("""
## Vorgehensweise
1. Filial-ID auswählen.
2. Auf "Berechne Vorhersage" klicken.
""")
    