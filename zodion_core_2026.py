import streamlit as st
from PIL import Image
import datetime

# --- LOGÍSTICA DE IMPORTACIÓN ---
try:
    from fpdf2 import FPDF
    PDF_DISPONIBLE = True
except:
    PDF_DISPONIBLE = False

try:
    import google.generativeai as genai
except ImportError:
    st.error("Crítico: Falta google-generativeai.")
    st.stop()

# --- INFRAESTRUCTURA ZODION ---
st.set_page_config(page_title="ZODION - Sistema de Auditoría", layout="wide", page_icon="🛡️")

# CLAVE DIRECTA
API_KEY = "AIzaSyD9StlzJy9FXg9epKfSgrWWPz5ZMzgCmNI"
genai.configure(api_key=API_KEY)

# CAMBIO DE MODELO A PRO PARA MÁXIMA ESTABILIDAD
try:
    model = genai.GenerativeModel('gemini-1.5-pro')
except:
    model = genai.GenerativeModel('gemini-pro-vision')

st.title("🛡️ Auditoría Sanitaria de Élite - ZODION")
st.markdown("---")

# --- MOTOR DE ANÁLISIS ---
foto = st.file_uploader("Cargar evidencia fotográfica", type=["jpg", "png", "jpeg"])

if foto:
    st.image(foto, width=500)
    if st.button("ANALIZAR CON IA DE ÉLITE"):
        with st.spinner("Zodion está procesando la imagen..."):
            try:
                img = Image.open(foto)
                # Forzamos la generación de contenido
                res = model.generate_content(["Analiza riesgos sanitarios BPM en esta imagen para Zodion.", img])
                st.session_state.res_ia = res.text
                st.success("Análisis Completado con Éxito")
            except Exception as e:
                st.error(f"Error técnico en el modelo: {e}")

if 'res_ia' in st.session_state:
    st.info(st.session_state.res_ia)
    
    # --- RESTAURACIÓN DE FUNCIÓN PDF ---
    st.subheader("📝 Generar Reporte")
    h = st.text_input("Hallazgo")
    a = st.text_input("Acción")
    
    if st.button("Descargar Reporte"):
        if PDF_DISPONIBLE:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("helvetica", 'B', 16)
            pdf.cell(0, 10, "ZODION SERVICIOS AMBIENTALES", 0, 1, 'C')
            pdf.set_font("helvetica", '', 12)
            pdf.ln(10)
            pdf.multi_cell(0, 10, f"HALLAZGO: {h}\nACCIÓN: {a}")
            pdf.ln(5)
            pdf.multi_cell(0, 10, f"ANÁLISIS IA:\n{st.session_state.res_ia}".encode('latin-1', 'replace').decode('latin-1'))
            
            st.download_button("Bajar PDF", pdf.output(), f"Reporte_{datetime.date.today()}.pdf")
        else:
            st.error("Función de PDF no disponible en este entorno local.")
