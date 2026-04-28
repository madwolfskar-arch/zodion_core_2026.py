import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Identidad Zodion
st.set_page_config(page_title="ZODION - Auditoría", layout="wide")
st.title("🛡️ ZODION SERVICIOS AMBIENTALES")

# 2. Conexión IA (Secrets)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Usamos gemini-1.5-flash que es el más rápido y estable para imágenes
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Configure su API KEY en Secrets de Streamlit")
    st.stop()

# 3. Interfaz
cliente = st.text_input("Cliente")
area = st.text_input("Área")
foto = st.file_uploader("Evidencia", type=["jpg", "png", "jpeg"])

if foto:
    # Mostramos la imagen al CEO
    img = Image.open(foto)
    st.image(img, width=400, caption="Vista previa de evidencia")
    
    if st.button("ANALIZAR AHORA"):
        with st.spinner("Procesando bajo parámetros Zodion..."):
            try:
                # --- SOLUCIÓN AL INVALID ARGUMENT ---
                # Re-abrimos la imagen para asegurar que el buffer esté limpio
                img_analisis = Image.open(foto)
                
                # Ejecución del motor
                res = model.generate_content([
                    "Como experto en BPM de Zodion, analiza los riesgos sanitarios y presencia de plagas en esta imagen de inspección.", 
                    img_analisis
                ])
                
                if res.text:
                    st.session_state.analisis = res.text
                    st.success("Análisis completado exitosamente.")
                else:
                    st.warning("La IA no pudo generar una respuesta clara. Intente con otra toma.")
                    
            except Exception as e:
                st.error(f"Falla en el motor de IA: {e}")
                st.info("Sugerencia: Refresque la página y asegúrese de que la foto no sea demasiado pesada (>5MB).")

# 4. Reporte Independiente (HTML para evitar NameError)
if 'analisis' in st.session_state:
    st.markdown("---")
    st.subheader("Resultados del Análisis Técnico")
    st.write(st.session_state.analisis)
    
    reporte_html = f"""
    <div style="font-family: Arial; border: 3px solid #003366; padding: 25px;">
        <h1 style="color: #003366; text-align: center;">ZODION SERVICIOS AMBIENTALES</h1>
        <h2 style="text-align: center;">INFORME DE INSPECCIÓN BPM</h2>
        <hr>
        <p><b>ESTABLECIMIENTO:</b> {cliente}</p>
        <p><b>ÁREA AUDITADA:</b> {area}</p>
        <p><b>HALLAZGOS TÉCNICOS:</b></p>
        <p style="background: #f9f9f9; padding: 10px;">{st.session_state.analisis}</p>
        <hr>
        <p style="font-size: 11px;">Documento generado por Zodion Core 2026 - Pasto, Colombia.</p>
    </div>
    """
    
    st.download_button(
        label="⬇️ DESCARGAR REPORTE PROFESIONAL",
        data=reporte_html,
        file_name=f"Zodion_{cliente}.html",
        mime="text/html"
    )
