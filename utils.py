import pandas as pd
import folium
from streamlit_folium import st_folium

def procesar_excel(file):
    df = pd.read_excel(file)
    # Aquí incluirías lógica para validar y preparar los datos
    return df

def exportar_rutas(servicios):
    # Lógica simplificada para agrupar servicios (a modo de demo)
    servicios["Vehículo"] = servicios.index % 15  # asignación básica
    resumen = servicios.groupby("Vehículo").agg({"Hora": ["min", "max"], "Origen": "count"})
    return servicios, resumen

def mostrar_mapa(servicios):
    m = folium.Map(location=[41.387, 2.17], zoom_start=12)
    for _, row in servicios.iterrows():
        folium.Marker(location=[41.387, 2.17], popup=row["Origen"]).add_to(m)
    st_folium(m, width=700)