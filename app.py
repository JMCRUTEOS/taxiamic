import streamlit as st
from utils import procesar_excel, mostrar_mapa, exportar_rutas

st.set_page_config(page_title="PMR Ruteos JMC", layout="wide")
st.title("🚌 PMR Ruteos JMC — Planificador de rutas")

uploaded_file = st.file_uploader("Sube tu archivo Excel de servicios", type=["xlsx"])

if uploaded_file:
    servicios = procesar_excel(uploaded_file)
    rutas, resumen = exportar_rutas(servicios)
    mostrar_mapa(rutas)
    st.download_button("Descargar ruteo (Excel)", data=rutas.to_excel(), file_name="ruteo.xlsx")
    st.dataframe(resumen)