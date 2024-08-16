import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.title("Análisis de Dispersión de Acciones")

# Entradas del usuario
ticker = st.text_input("Ingrese el ticker del activo:", value="AAPL")
period = st.selectbox("Seleccione el periodo:", ["1y", "5y", "10y", "max"], index=2)
sma_window = st.slider("Seleccione la ventana de SMA:", min_value=5, max_value=100, value=21)

# Descargar datos históricos
data = yf.download(ticker, period=period)

# Calcular la SMA
data['SMA'] = data['Close'].rolling(window=sma_window).mean()

# Calcular la Dispersión
data['Dispersión'] = (data['Close'] - data['SMA']) / data['SMA'] * 100

# Eliminar filas con valores NaN
data = data.dropna()

# Separar dispersiones positivas y negativas
positivas = data['Dispersión'][data['Dispersión'] > 0]
negativas = data['Dispersión'][data['Dispersión'] < 0]

# Calcular percentiles
percentiles_positivos = np.percentile(positivas, [5, 10, 25, 50, 75, 90, 97])
percentiles_negativos = np.percentile(negativas, [5, 10, 25, 50, 75, 90, 97])

# Mostrar percentiles
st.subheader(f"Percentiles de Dispersión Positiva para {ticker} ({period}):")
st.write(f"5%: {percentiles_positivos[0]:.2f}%")
st.write(f"10%: {percentiles_positivos[1]::.2f}%")
st.write(f"25%: {percentiles_positivos[2]:.2f}%")
st.write(f"50%: {percentiles_positivos[3]:.2f}%")
st.write(f"75%: {percentiles_positivos[4]:.2f}%")
st.write(f"90%: {percentiles_positivos[5]:.2f}%")
st.write(f"97%: {percentiles_positivos[6]:.2f}%")

st.subheader(f"Percentiles de Dispersión Negativa para {ticker} ({period}):")
st.write(f"5%: {percentiles_negativos[0]:.2f}%")
st.write(f"10%: {percentiles_negativos[1]:.2f}%")
st.write(f"25%: {percentiles_negativos[2]:.2f}%")
st.write(f"50%: {percentiles_negativos[3]:.2f}%")
st.write(f"75%: {percentiles_negativos[4]:.2f}%")
st.write(f"90%: {percentiles_negativos[5]:.2f}%")
st.write(f"97%: {percentiles_negativos[6]:.2f}%")

# Estadísticas adicionales
st.subheader("Estadísticas adicionales:")
st.write(f"Número total de días analizados: {len(data)}")
st.write(f"Días con dispersión positiva: {len(positivas)} ({len(positivas)/len(data)*100:.2f}%)")
st.write(f"Días con dispersión negativa: {len(negativas)} ({len(negativas)/len(data)*100:.2f}%)")
st.write(f"Dispersión positiva máxima: {positivas.max():.2f}%")
st.write(f"Dispersión negativa máxima: {negativas.min():.2f}%")

# Graficar histograma interactivo con Plotly
st.subheader(f"Distribución de Dispersión para {ticker} ({period})")

fig = go.Figure()

# Graficar dispersión positiva
fig.add_trace(go.Histogram(
    x=positivas,
    nbinsx=100,
    name='Dispersión Positiva',
    marker_color='green',
    opacity=0.5,
    hovertemplate='Dispersión: %{x:.2f}%<extra></extra>'
))

# Graficar dispersión negativa
fig.add_trace(go.Histogram(
    x=negativas,
    nbinsx=100,
    name='Dispersión Negativa',
    marker_color='red',
    opacity=0.5,
    hovertemplate='Dispersión: %{x:.2f}%<extra></extra>'
))

# Añadir líneas verticales para los percentiles positivos
for p in percentiles_positivos:
    fig.add_vline(x=p, line_dash='dash', line_color='darkgreen', opacity=0.7)

# Añadir líneas verticales para los percentiles negativos
for p in percentiles_negativos:
    fig.add_vline(x=p, line_dash='dash', line_color='darkred', opacity=0.7)

fig.update_layout(
    title=f'Distribución de Dispersión para {ticker}',
    xaxis_title='Porcentaje de Dispersión',
    yaxis_title='Frecuencia',
    barmode='overlay',
    hovermode='x'
)

st.plotly_chart(fig, use_container_width=True)

