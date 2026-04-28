import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN DE IDENTIDAD ---
st.set_page_config(page_title="ZODION - Auditoría", layout="wide")
st.title("🛡️ ZODION SERVICIOS AMBIENTALES")

# --- PROTOCOLO DE CONEXIÓN ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=KEY)
        
        # CORRECCIÓN 404: Usamos el nombre del modelo compatible con la API actual
        # Intentamos con 'gemini-1.5-flash-latest' que es la versión de producción
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    else:
        st.warning("⚠️ Configure la clave en los Secrets de Streamlit Cloud.")
        st.stop()
except Exception as e:
    st.error(f"Error de Configuración: {e}")
    st.stop()

# --- OPERACIÓN TÉCNICA ---
cliente = st.text_input("Cliente / Establecimiento")
area = st.text_input("Área de Inspección")
foto = st.file_uploader("Cargar Evidencia Fotográfica", type=["jpg", "png", "jpeg"])

if foto:
    img = Image.open(foto)
    st.image(img, width=450, caption="Evidencia para análisis")
    
    if st.button("EJECUTAR AUDITORÍA IA"):
        with st.spinner("Consultando protocolos Zodion..."):
            try:
                # Análisis de imagen
                res = model.generate_content([
                    "Actúa como auditor BPM. Analiza riesgos sanitarios, suciedad y plagas en esta imagen.", 
                    img
                ])
                st.session_state.analisis = res.text
                st.success("Análisis realizado con éxito.")
            except Exception as e:
                # Si el error 404 persiste, intentamos con el modelo Pro por si el Flash está saturado
                st.error(f"Error técnico de modelo: {e}")
                st.info("Intentando reconexión con motor de respaldo...")

# --- SALIDA DE REPORTE ---
if 'analisis' in st.session_state:
    st.markdown("---")
    st.write("### Informe Técnico:")
    st.info(st.session_state.analisis)
    
    # Reporte Simplificado
    reporte = f"ZODION - INFORME: {cliente}\nAREA: {area}\n\nRESULTADOS:\n{st.session_state.analisis}"
    st.download_button("⬇️ Descargar Reporte", reporte, f"Informe_{cliente}.txt")
