import streamlit as st
from PIL import Image
import google.generativeai as genai
from fpdf2 import FPDF
import datetime

# --- CONFIGURACIÓN DE MARCA ZODION ---
st.set_page_config(page_title="ZODION - Sistema de Auditoría BPM", layout="wide")

# Conexión Segura (Motor Gemini Pro)
API_KEY = "AIzaSyD9StlzJy9FXg9epKfSgrWWPz5ZMzgCmNI"
genai.configure(api_key=API_KEY)
# Usamos el modelo 'gemini-pro-vision' que es el más estable para análisis técnico de imágenes
model = genai.GenerativeModel('gemini-1.0-pro-vision')

# --- MOTOR DE GENERACIÓN DE DOCUMENTOS (IDENTIDAD ZODION) ---
class ReporteZodion(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "ZODION SERVICIOS AMBIENTALES - NARIÑO", 0, 1, "C")
        self.set_font("helvetica", "I", 10)
        self.cell(0, 5, "Sistemas de Gestión de Inocuidad y BPM", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()} - Documento Técnico Confidencial", 0, 0, "C")

# --- INTERFAZ PROFESIONAL ---
st.title("🛡️ Sistema de Auditoría Sanitaria de Élite")
st.info("Plataforma técnica para la generación de reportes BPM bajo parámetros Zodion.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Parámetros de Inspección")
    cliente = st.text_input("Nombre del Establecimiento")
    area = st.text_input("Área / Sección Auditada")
    
    st.markdown("---")
    st.write("**Checklist Zodion (Cumplimiento BPM)**")
    c1 = st.checkbox("Higiene de superficies y equipos")
    c2 = st.checkbox("Ausencia de focos de plagas (Blattella/Rodentia)")
    c3 = st.checkbox("Rotulación y trazabilidad de insumos")
    
    foto = st.file_uploader("Evidencia Fotográfica", type=["jpg", "png", "jpeg"])

with col2:
    st.subheader("🤖 Análisis de IA Especializada")
    if foto:
        img = Image.open(foto)
        st.image(img, use_container_width=True)
        
        if st.button("ANALIZAR BAJO NORMATIVA ZODION"):
            with st.spinner("Ejecutando protocolo de análisis técnico..."):
                try:
                    # Prompt especializado que considera parámetros Zodion
                    instruccion = f"""
                    Actúa como experto en BPM y saneamiento ambiental de Zodion. 
                    Analiza esta imagen del área {area} en {cliente}.
                    Evalúa: 1. Riesgos de contaminación, 2. Evidencia de plagas, 3. Estado de limpieza.
                    Genera un análisis técnico formal y acciones correctivas.
                    """
                    response = model.generate_content([instruccion, img])
                    st.session_state.analisis_ia = response.text
                    st.success("Análisis completado satisfactoriamente.")
                except Exception as e:
                    st.error(f"Error de comunicación con el motor IA: {e}")

# --- RESULTADOS Y GENERACIÓN DE PDF ---
if 'analisis_ia' in st.session_state:
    st.divider()
    st.write("### Resultados del Análisis Técnico")
    st.write(st.session_state.analisis_ia)
    
    st.markdown("---")
    st.subheader("📄 Generación de Entregable Profesional")
    hallazgo = st.text_area("Hallazgo final del Auditor", value="Se observa incumplimiento en los protocolos de limpieza...")
    accion = st.text_area("Acción correctiva inmediata")
    
    if st.button("GENERAR PDF PROFESIONAL"):
        pdf = ReporteZodion()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, f"REPORTE DE INSPECCIÓN - {datetime.date.today()}", 0, 1)
        pdf.set_font("helvetica", "", 11)
        pdf.cell(0, 7, f"Cliente: {cliente}", 0, 1)
        pdf.cell(0, 7, f"Área: {area}", 0, 1)
        pdf.ln(5)
        
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 7, "Análisis de Riesgos (IA Zodion):", 0, 1)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 6, st.session_state.analisis_ia.encode('latin-1', 'replace').decode('latin-1'))
        
        pdf.ln(5)
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 7, "Conclusiones y Acciones:", 0, 1)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 6, f"Hallazgo: {hallazgo}\nAcción: {accion}".encode('latin-1', 'replace').decode('latin-1'))
        
        st.download_button(
            label="⬇️ Descargar Reporte PDF de Élite",
            data=pdf.output(),
            file_name=f"Zodion_Reporte_{cliente}.pdf",
            mime="application/pdf"
        )
