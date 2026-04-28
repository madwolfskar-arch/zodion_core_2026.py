import streamlit as st
import datetime
from PIL import Image
try:
    import google.generativeai as genai
    from fpdf2 import FPDF
except ImportError:
    st.error("Instalando suministros médicos... por favor espere 30 segundos y refresque.")

# --- CONFIGURACIÓN DE MARCA ZODION ---
st.set_page_config(page_title="ZODION - Sistema de Auditoría BPM", layout="wide", page_icon="🛡️")

# Conexión Segura vía Secrets de Streamlit
# IMPORTANTE: En la nube no pondremos la clave aquí, la leerá de la configuración
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error de configuración de credenciales en la nube.")

# --- MOTOR DE REPORTES ZODION ---
class ReporteZodion(FPDF):
    def header(self):
        # Membrete institucional
        self.set_font("helvetica", "B", 15)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "ZODION SERVICIOS AMBIENTALES - NARIÑO", 0, 1, "C")
        self.set_font("helvetica", "I", 10)
        self.cell(0, 5, "Líderes en Saneamiento Ambiental e Inocuidad", 0, 1, "C")
        self.ln(10)

# --- INTERFAZ PROFESIONAL ---
st.title("🛡️ Sistema de Auditoría Sanitaria de Élite")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Datos de la Inspección Técnica")
    cliente = st.text_input("Nombre del Establecimiento / Cliente")
    area = st.text_input("Área o Sección Auditada")
    
    st.write("**Checklist Técnico Zodion**")
    c1 = st.checkbox("Higiene de superficies y equipos")
    c2 = st.checkbox("Control de plagas (Blattella/Rodentia)")
    c3 = st.checkbox("Gestión de residuos y trazabilidad")
    
    foto = st.file_uploader("Evidencia Fotográfica de Campo", type=["jpg", "png", "jpeg"])

with col2:
    st.subheader("🤖 Análisis de IA Especializada")
    if foto:
        img = Image.open(foto)
        st.image(img, use_container_width=True, caption="Evidencia cargada")
        
        if st.button("EJECUTAR ANÁLISIS BPM PROFESIONAL"):
            with st.spinner("IA Zodion evaluando riesgos bajo normativa..."):
                try:
                    # Prompt de análisis profundo
                    prompt = f"""
                    Actúa como un Auditor Senior de Zodion. Analiza esta imagen de {area} en {cliente}.
                    1. Identifica riesgos sanitarios críticos (BPM).
                    2. Detecta indicios de plagas o fallas de hermeticidad.
                    3. Evalúa el estado de limpieza y desinfección.
                    Proporciona un informe técnico detallado y acciones correctivas.
                    """
                    response = model.generate_content([prompt, img])
                    st.session_state.analisis_ia = response.text
                    st.success("Análisis completado.")
                except Exception as e:
                    st.error(f"Error técnico: {e}")

if 'analisis_ia' in st.session_state:
    st.divider()
    st.subheader("📝 Resultados y Conclusiones")
    st.info(st.session_state.analisis_ia)
    
    h = st.text_area("Hallazgo del Auditor", "Se detecta...")
    a = st.text_area("Acción Correctiva Sugerida", "Realizar limpieza profunda...")

    if st.button("GENERAR DOCUMENTO PDF PROFESIONAL"):
        pdf = ReporteZodion()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, f"REPORTE TÉCNICO - {datetime.date.today()}", 0, 1)
        pdf.set_font("helvetica", "", 11)
        pdf.cell(0, 7, f"Establecimiento: {cliente}", 0, 1)
        pdf.cell(0, 7, f"Área inspeccionada: {area}", 0, 1)
        pdf.ln(5)
        
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 7, "Evaluación de Inteligencia Artificial:", 0, 1)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 6, st.session_state.analisis_ia.encode('latin-1', 'replace').decode('latin-1'))
        
        pdf.ln(5)
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 7, "Conclusiones Finales:", 0, 1)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 6, f"HALLAZGO: {h}\nACCIÓN: {a}".encode('latin-1', 'replace').decode('latin-1'))
        
        st.download_button(
            label="⬇️ Descargar Reporte PDF de Élite",
            data=pdf.output(),
            file_name=f"Reporte_Zodion_{cliente}.pdf",
            mime="application/pdf"
        ) 
