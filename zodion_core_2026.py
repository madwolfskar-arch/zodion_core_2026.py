import streamlit as st
import requests
import base64

# 1. Configuración de Marca Zodion
st.set_page_config(page_title="ZODION - Auditoría", layout="wide")
st.title("🛡️ ZODION SERVICIOS AMBIENTALES")

# 2. Clave de los Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. Interfaz de Usuario
cliente = st.text_input("Establecimiento")
area = st.text_input("Área Inspeccionada")
foto = st.file_uploader("Evidencia Fotográfica", type=["jpg", "png", "jpeg"])

if foto and API_KEY:
    bytes_data = foto.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    st.image(bytes_data, width=400, caption="Evidencia cargada")

    if st.button("EJECUTAR ANÁLISIS DE ÉLITE"):
        with st.spinner("IA Zodion accediendo a servidores estables..."):
            
            # --- CAMBIO DE COORDENADAS (v1 y gemini-1.5-flash-latest) ---
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": f"Actúa como auditor BPM senior de Zodion. Analiza riesgos sanitarios y plagas en esta área de {area} para el cliente {cliente}."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}}
                    ]
                }]
            }
            
            try:
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    resultado = response.json()
                    # Extraemos el texto de la respuesta estructurada
                    texto_analisis = resultado['candidates'][0]['content']['parts'][0]['text']
                    st.session_state.analisis = texto_analisis
                    st.success("Conexión establecida y análisis completado.")
                else:
                    st.error(f"Error del servidor de Google ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Falla de red: {e}")

# 4. Reporte Final
if 'analisis' in st.session_state:
    st.markdown("---")
    st.markdown("### 📋 Resultados del Análisis Técnico")
    st.info(st.session_state.analisis)
    
    reporte = f"REPORTE ZODION\nCliente: {cliente}\nArea: {area}\n\nAnalisis:\n{st.session_state.analisis}"
    st.download_button("⬇️ Descargar Informe .txt", reporte, f"Informe_Zodion_{cliente}.txt")
