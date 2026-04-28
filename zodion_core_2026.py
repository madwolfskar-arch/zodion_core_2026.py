import streamlit as st
import requests
import base64

# 1. Marca Institucional
st.set_page_config(page_title="ZODION - Auditoría", layout="wide")
st.title("🛡️ ZODION SERVICIOS AMBIENTALES")

# 2. Credenciales
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. Panel de Control
cliente = st.text_input("Establecimiento")
area = st.text_input("Área Inspeccionada")
foto = st.file_uploader("Evidencia Fotográfica", type=["jpg", "png", "jpeg"])

if foto and API_KEY:
    bytes_data = foto.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    st.image(bytes_data, width=400, caption="Evidencia cargada")

    if st.button("EJECUTAR ANÁLISIS DE ÉLITE"):
        with st.spinner("IA Zodion conectando con motor de respaldo..."):
            
            # --- RUTA DE PRODUCCIÓN ACTUALIZADA ---
            # Cambiamos a 'gemini-1.5-flash' sin prefijos experimentales
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            # Si el anterior falló, este formato de payload es el estándar global
            payload = {
                "contents": [{
                    "parts": [
                        {"text": f"Analiza esta imagen como auditor de Zodion. Detecta riesgos BPM, suciedad y plagas en {area} para {cliente}."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}}
                    ]
                }]
            }
            
            try:
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    resultado = response.json()
                    texto_analisis = resultado['candidates'][0]['content']['parts'][0]['text']
                    st.session_state.analisis = texto_analisis
                    st.success("Análisis completado con éxito.")
                else:
                    # TÁCTICA DE RESPALDO: Si falla el Flash, intentamos con el modelo Pro automáticamente
                    url_pro = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={API_KEY}"
                    response = requests.post(url_pro, json=payload)
                    if response.status_code == 200:
                        resultado = response.json()
                        st.session_state.analisis = resultado['candidates'][0]['content']['parts'][0]['text']
                        st.success("Análisis completado (Motor Pro).")
                    else:
                        st.error(f"Error persistente de Google: {response.status_code}. Verifique su cuota en AI Studio.")
            except Exception as e:
                st.error(f"Falla de red Zodion: {e}")

# 4. Entrega de Resultados
if 'analisis' in st.session_state:
    st.markdown("---")
    st.info(st.session_state.analisis)
    
    reporte = f"REPORTE ZODION\nCliente: {cliente}\nArea: {area}\n\nAnalisis:\n{st.session_state.analisis}"
    st.download_button("⬇️ Descargar Reporte Técnico", reporte, f"Informe_Zodion_{cliente}.txt")
