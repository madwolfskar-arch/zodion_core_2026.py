import streamlit as st
import requests
import base64

st.set_page_config(page_title="ZODION - Auditoría", layout="wide")
st.title("🛡️ ZODION SERVICIOS AMBIENTALES")

API_KEY = st.secrets.get("GOOGLE_API_KEY")

cliente = st.text_input("Establecimiento")
area = st.text_input("Área Inspeccionada")
foto = st.file_uploader("Evidencia Fotográfica", type=["jpg", "png", "jpeg"])

if foto and API_KEY:
    bytes_data = foto.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    st.image(bytes_data, width=400)

    if st.button("EJECUTAR ANÁLISIS DE ÉLITE"):
        with st.spinner("Escaneando servidores de Google..."):
            
            # PASO 1: Listar modelos disponibles para SU llave
            list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
            models_resp = requests.get(list_url)
            
            try:
                available_models = models_resp.json().get('models', [])
                # Buscamos cualquier modelo que soporte generación de contenido y visión
                target_model = None
                for m in available_models:
                    if "generateContent" in m['supportedGenerationMethods'] and "gemini" in m['name']:
                        target_model = m['name']
                        break
                
                if not target_model:
                    st.error("No se encontraron modelos activos en su cuenta de AI Studio.")
                    st.stop()
                
                # PASO 2: Ejecutar con el modelo encontrado
                st.info(f"Conectado a motor: {target_model}")
                gen_url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={API_KEY}"
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": f"Analiza riesgos sanitarios BPM en {area} para {cliente}."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}}
                        ]
                    }]
                }
                
                res = requests.post(gen_url, json=payload)
                if res.status_code == 200:
                    st.session_state.analisis = res.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("Análisis exitoso.")
                else:
                    st.error(f"Falla final: {res.text}")
            except Exception as e:
                st.error(f"Error de sistema: {e}")

if 'analisis' in st.session_state:
    st.info(st.session_state.analisis)
    st.download_button("Descargar Informe", st.session_state.analisis, f"Zodion_{cliente}.txt")
