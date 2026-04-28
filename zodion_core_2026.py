import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf2 import FPDF
import datetime

# 1. Identidad
st.set_page_config(page_title="ZODION - Auditoría", layout="wide")
st.title("🛡️ ZODION SERVICIOS AMBIENTALES")

# 2. Conexión IA (Secrets)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Configure su API KEY en Secrets")

# 3. Operación
col1, col2 = st.columns(2)
with col1:
    cliente = st.text_input("Cliente")
    area = st.text_input("Área")
    foto = st.file_uploader("Evidencia", type=["jpg", "png", "jpeg"])

with col2:
    if foto:
        img = Image.open(foto)
        st.image(img, use_container_width=True)
        if st.button("ANALIZAR"):
            res = model.generate_content(["Analiza riesgos BPM en esta imagen.", img])
            st.session_state.analisis = res.text

# 4. Reporte PDF
if 'analisis' in st.session_state:
    st.info(st.session_state.analisis)
    if st.button("DESCARGAR REPORTE"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "ZODION - REPORTE TECNICO", 0, 1, "C")
        pdf.set_font("helvetica", "", 10)
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Cliente: {cliente}\nArea: {area}\n\nAnalisis:\n{st.session_state.analisis}".encode('latin-1', 'replace').decode('latin-1'))
        st.download_button("Bajar Archivo PDF", pdf.output(), f"Reporte_{cliente}.pdf")
