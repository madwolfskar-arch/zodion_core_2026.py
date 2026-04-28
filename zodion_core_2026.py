import streamlit as st
import requests
import base64

# 1. Configuración de Marca
st.set_page_config(page_title="ZODION - Auditoría", layout="wide")
st.title("🛡️ ZODION SERVICIOS AMBIENTALES")

# 2. Obtener la llave de los Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. Interfaz de Usuario
cliente = st.text_input("Establecimiento")
area = st.text_input("Área Inspeccionada")
foto = st.file_uploader("Evidencia Fotográfica", type=["jpg", "png", "jpeg"])

if foto and API_KEY:
    # Preparar la imagen para enviarla sin librerías pesadas
    bytes_data = foto.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    st.image(bytes_data, width=400)

    if st.button("EJECUTAR ANÁLISIS DE ÉLITE"):
        with st.spinner("IA Zodion analizando riesgos..."):
            # Conexión directa vía API REST (No necesita google-generativeai)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": f"Actúa como auditor BPM senior. Analiza riesgos sanitarios, plagas y limpieza en esta área de {area} para el cliente {cliente}."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}}
                    ]
                }]
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                resultado = response.json()
                texto_analisis = resultado['candidates'][0]['content']['parts'][0]['text']
                st.session_state.analisis = texto_analisis
                st.success("Análisis completado.")
            else:
                st.error(f"Error de conexión: {response.text}")

# 4. Reporte Final
if 'analisis' in st.session_state:
    st.markdown("---")
    st.info(st.session_state.analisis)
    
    # Reporte simple que no falla
    reporte = f"REPORTE ZODION\nCliente: {cliente}\nArea: {area}\n\nAnalisis:\n{st.session_state.analisis}"
    st.download_button("Descargar Informe Técnico", reporte, f"Informe_Zodion_{cliente}.txt")
