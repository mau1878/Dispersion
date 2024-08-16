import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title("Análisis de Dispersión de Acciones")

# Entradas del usuario
ticker = st.text_input("Ingrese el ticker del activo:", value="AAPL")
period = st.selectbox("Seleccione el periodo:", ["1y", "5y", "10y", "max"], index=2)
sma_window = st.slider("Seleccione la ventana de SMA:", min_value=5, max_value=100, value=21)

# Descargar datos históricos
try:
    data = yf.download(ticker, period=period)
except Exception as e:
    st.error(f"Error al descargar los datos: {e}")
    st.stop()

# Calcular la SMA
data['SMA'] = data['Close'].rolling(window=sma_window).mean()

# Calcular la Dispersión
data['Dispersión'] = (data['Close'] - data['SMA']) / data['SMA'] * 100

# Eliminar filas con valores NaN
data = data.dropna()

# Graficar con Plotly
fig = px.histogram(data, x='Dispersión', color_discrete_sequence=['green' if p > 0 else 'red' for p in data['Dispersión']],
                   labels={'Dispersión': 'Porcentaje de Dispersión'},
                   title=f'Distribución de Dispersión para {ticker}')

st.plotly_chart(fig)

