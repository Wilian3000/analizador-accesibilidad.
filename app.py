import streamlit as st
from accesibilidad_analizador import analizar_accesibilidad
import json

st.set_page_config(page_title="Analizador de Accesibilidad Web", layout="centered")
st.title("🔎 Evaluador de Accesibilidad con IA - Módulo 1")
st.markdown("Analiza si una página web tiene imágenes sin texto alternativo y formularios sin etiquetas.")

url = st.text_input("🔗 Ingresa la URL a analizar", "https://www.example.com")

if st.button("Analizar"):
    with st.spinner("Analizando..."):
        resultado = analizar_accesibilidad(url)

    if "error" in resultado:
        st.error(f"Error al procesar la URL: {resultado['error']}")
    else:
        st.success(f"Análisis completado. Se encontraron {resultado['total_errores']} posibles problemas.")

        st.subheader("❌ Imágenes sin atributo alt:")
        if resultado["imagenes_sin_alt"]:
            for i, img in enumerate(resultado["imagenes_sin_alt"], 1):
                st.code(f"{i}. {img}", language="html")
        else:
            st.info("Todas las imágenes tienen atributo alt.")

        st.subheader("❌ Campos de formulario sin etiqueta (label):")
        if resultado["campos_sin_label"]:
            for i, campo in enumerate(resultado["campos_sin_label"], 1):
                st.code(f"{i}. {campo}", language="html")
        else:
            st.info("Todos los campos tienen etiquetas.")

        st.download_button("📄 Descargar reporte JSON", data=json.dumps(resultado, indent=4), file_name="reporte_accesibilidad.json", mime="application/json")
