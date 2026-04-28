import streamlit as st
from PIL import Image
import google.generativeai as genai
import datetime
from fpdf2 import FPDF

# --- INICIO DE INFRAESTRUCTURA ZODION ---
st.set_page_config(page_title="ZODION - Sistema de Auditoría", layout="wide", page_icon="🛡️")

# Conexión Segura
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error de configuración en Secrets.")

# --- GENERADOR DE REPORTES ---
class ZodionPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'ZODION SERVICIOS AMBIENTALES - REPORTE BPM', 0, 1, 'C')
        self.ln(5)

def crear_pdf(checklist, analisis, hallazgo, accion):
    pdf = ZodionPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(0, 10, "RESULTADOS DE INSPECCIÓN", 0, 1)
    pdf.set_font("helvetica", '', 10)
    for k, v in checklist.items():
        pdf.cell(0, 7, f"{k}: {'CUMPLE' if v else 'NO CUMPLE'}", 0, 1)
    pdf.ln(5)
    pdf.multi_cell(0, 7, f"ANÁLISIS IA: {analisis}".encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)
    pdf.multi_cell(0, 7, f"ACCIONES: {hallazgo} - {accion}".encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output()

# --- INTERFAZ ---
st.title("🛡️ Auditoría Sanitaria de Élite")

with st.sidebar:
    st.header("Checklist Técnico")
    c1 = st.checkbox("Limpieza de áreas")
    c2 = st.checkbox("Control de plagas")
    c3 = st.checkbox("Rotulación/Lotes")
    checks = {"Limpieza": c1, "Plagas": c2, "Rotulación": c3}

foto = st.file_uploader("Evidencia Fotográfica", type=["jpg", "png", "jpeg"])

if foto:
    st.image(foto, width=400)
    if st.button("ANALIZAR EVIDENCIA"):
        img = Image.open(foto)
        res = model.generate_content(["Analiza riesgos sanitarios BPM en esta imagen para Zodion.", img])
        st.session_state.res_ia = res.text
        st.write(res.text)

st.divider()
h = st.text_input("Hallazgo")
a = st.text_input("Acción")

if st.button("GENERAR PDF"):
    pdf_out = crear_pdf(checks, st.session_state.get('res_ia', ''), h, a)
    st.download_button("Descargar Reporte", pdf_out, "Reporte_Zodion.pdf", "application/pdf")

    

        



