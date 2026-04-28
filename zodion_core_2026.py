import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN DE IDENTIDAD ---
st.set_page_config(page_title="ZODION - Auditoría", layout="wide")
st.title("🛡️ ZODION SERVICIOS AMBIENTALES")

# --- PROTOCOLO DE CONEXIÓN SEGURO ---
try:
    # Intentamos leer la clave desde los Secrets de Streamlit
    if "GOOGLE_API_KEY" in st.secrets:
        KEY = st.secrets["GOOGLE_API_KEY"]
    else:
        # Si no está en Secrets, la pedimos manualmente para no detener la operación
        KEY = st.sidebar.text_input("Introduzca Clave de Respaldo (API KEY):", type="password")

    if KEY:
        genai.configure(api_key=KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.warning("⚠️ Esperando configuración de API KEY en Secrets...")
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
                # Análisis forzado de imagen limpia
                res = model.generate_content([
                    "Analiza esta imagen como auditor de saneamiento. Identifica riesgos BPM, suciedad y plagas.", 
                    img
                ])
                st.session_state.analisis = res.text
                st.success("Análisis realizado con éxito.")
            except Exception as e:
                st.error(f"Error de Validación de Llave: {e}")
                st.info("Sugerencia: Verifique que la API KEY en Secrets sea la correcta.")

# --- SALIDA DE REPORTE ---
if 'analisis' in st.session_state:
    st.markdown("---")
    st.write("### Informe Técnico:")
    st.info(st.session_state.analisis)
    
    # Generador de reporte directo
    reporte = f"ZODION - INFORME: {cliente}\nAREA: {area}\n\nRESULTADOS:\n{st.session_state.analisis}"
    st.download_button("⬇️ Descargar Reporte Técnico", reporte, f"Informe_{cliente}.txt")
