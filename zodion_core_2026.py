import streamlit as st
import datetime

# --- BLOQUE DE IMPORTACIÓN FORZADA (CONTROL DE LOGÍSTICA) ---
try:
    from fpdf2 import FPDF
    from PIL import Image
    import google.generativeai as genai
except ImportError as e:
    st.error(f"❌ Error Crítico de Suministros: Falta la librería {e.name}. Verifique su archivo requirements.txt.")
    st.stop()

# --- INICIO DE INFRAESTRUCTURA ZODION ---
st.set_page_config(page_title="ZODION - Sistema de Auditoría", layout="wide", page_icon="🛡️")
# --- CONEXIÓN SEGURA (BYPASS LOCAL) ---
# En la nube usaremos st.secrets, en local usamos la clave directa
API_KEY = "AIzaSyD9StlzJy9FXg9epKfSgrWWPz5ZMzgCmNI"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")



model = genai.GenerativeModel('gemini-1.5-flash')

# --- GENERADOR DE REPORTES (MOTOR PDF) ---
class ZodionPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(0, 51, 102)
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
    pdf.set_font("helvetica", 'B', 11)
    pdf.cell(0, 7, "ANÁLISIS DE INTELIGENCIA ARTIFICIAL:", 0, 1)
    pdf.set_font("helvetica", '', 10)
    pdf.multi_cell(0, 7, analisis.encode('latin-1', 'replace').decode('latin-1'))
    
    pdf.ln(5)
    pdf.set_font("helvetica", 'B', 11)
    pdf.cell(0, 7, "ACCIONES CORRECTIVAS RECOMENDADAS:", 0, 1)
    pdf.set_font("helvetica", '', 10)
    pdf.multi_cell(0, 7, f"HALLAZGO: {hallazgo}\nACCIÓN: {accion}".encode('latin-1', 'replace').decode('latin-1'))
    
    # Retornar como bytes para Streamlit
    return pdf.output()

# --- INTERFAZ DE USUARIO ---
st.title("🛡️ Auditoría Sanitaria de Élite")
st.markdown("---")

with st.sidebar:
    st.header("Checklist Técnico")
    c1 = st.checkbox("Higiene de áreas/equipos")
    c2 = st.checkbox("Control integral de plagas")
    c3 = st.checkbox("Rotulación y trazabilidad")
    checks = {"Limpieza": c1, "Plagas": c2, "Rotulación": c3}

col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Captura de Evidencia")
    foto = st.file_uploader("Cargar imagen de inspección", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto, use_container_width=True)

with col2:
    st.subheader("🤖 Análisis Técnico")
    if foto:
        if st.button("ANALIZAR EVIDENCIA"):
            with st.spinner("El sistema Zodion está evaluando riesgos..."):
                img = Image.open(foto)
                res = model.generate_content(["Analiza riesgos sanitarios BPM en esta imagen para Zodion. Evalúa limpieza, plagas y cumplimiento técnico.", img])
                st.session_state.res_ia = res.text
    
    if 'res_ia' in st.session_state:
        st.info(st.session_state.res_ia)

st.divider()
st.subheader("📝 Conclusiones Finales")
h = st.text_input("Hallazgo Técnico Detectado")
a = st.text_input("Acción Correctiva Sugerida")

if st.button("📄 GENERAR REPORTE PDF"):
    if 'res_ia' not in st.session_state:
        st.warning("Primero debe realizar el análisis de la imagen.")
    else:
        pdf_output = crear_pdf(checks, st.session_state.res_ia, h, a)
        st.download_button(
            label="⬇️ Descargar Reporte PDF",
            data=bytes(pdf_output), # Conversión explícita a bytes
            file_name=f"Zodion_Reporte_{datetime.date.today()}.pdf",
            mime="application/pdf"
        ) 
