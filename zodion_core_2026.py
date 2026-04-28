import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="ZODION - Auditoría", layout="wide")
st.title("🛡️ ZODION SERVICIOS AMBIENTALES")

# --- CONEXIÓN IA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error: Configure su API KEY en los Secrets de la App")

# --- OPERACIÓN ---
col1, col2 = st.columns(2)
with col1:
    cliente = st.text_input("Establecimiento")
    area = st.text_input("Área Inspeccionada")
    foto = st.file_uploader("Subir Evidencia", type=["jpg", "png", "jpeg"])

with col2:
    if foto:
        img = Image.open(foto)
        st.image(img, use_container_width=True)
        if st.button("ANALIZAR AHORA"):
            res = model.generate_content(["Analiza riesgos BPM y plagas en esta imagen.", img])
            st.session_state.analisis = res.text

# --- GENERADOR DE REPORTE INDEPENDIENTE ---
if 'analisis' in st.session_state:
    st.markdown("### Resultado del Análisis")
    st.info(st.session_state.analisis)
    
    # Creamos un reporte profesional en HTML (Se abre en Chrome/Edge y se guarda como PDF)
    reporte_final = f"""
    <div style="font-family: Arial; border: 2px solid #003366; padding: 20px;">
        <h1 style="color: #003366; text-align: center;">ZODION SERVICIOS AMBIENTALES</h1>
        <h3 style="text-align: center;">REPORTE TÉCNICO DE AUDITORÍA</h3>
        <hr>
        <p><b>CLIENTE:</b> {cliente}</p>
        <p><b>ÁREA:</b> {area}</p>
        <p><b>INFORME IA:</b></p>
        <p style="text-align: justify;">{st.session_state.analisis}</p>
        <hr>
        <p style="font-size: 12px; color: grey;">Generado por Zodion Core v2026 - Pasto, Nariño</p>
    </div>
    """
    
    st.download_button(
        label="⬇️ DESCARGAR REPORTE PROFESIONAL",
        data=reporte_final,
        file_name=f"Reporte_Zodion_{cliente}.html",
        mime="text/html"
    )
