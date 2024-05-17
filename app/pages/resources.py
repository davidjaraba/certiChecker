import base64

import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000/api"


def get_resource(resource_id):
    """Obtiene y muestra un certificado."""
    response = requests.get(f"{API_URL}/resources/{resource_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error al obtener el resource')
        return []


def get_company_urls(company_id):
    """Obtiene el URLs de los """
    response = requests.get(f"{API_URL}/urls/?company_id={company_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error al obtener')
        return []


def main():
    resource_id = st.query_params['id']
    resource = get_resource(resource_id)
    certificate = resource['certificate']
    data_cert = certificate['certificate']

    if resource:
        st.title(data_cert.get('name'))

        st.text('Encontrado el ' + certificate.get('found_date'))

        full_url = resource.get('full_url')
        st.markdown(f'<a href="{full_url}" target="_blank">Encontrado en la URL</a>', unsafe_allow_html=True)

        data_type = resource['type']
        path_file = resource['path_file']

        if data_type == 'TXT':
            try:
                # Abre y lee el contenido del archivo de texto
                with open('app/' + path_file, 'r', encoding='utf-8') as file:
                    content = file.read()

                # st.text_area('Encontrado en', content, height=500, disabled=True)

                # Resalta las palabras clave en el contenido (por ejemplo, "importante")
                highlighted_content = content.replace(data_cert.get('name'), f'<span style="background-color: yellow; '
                                                                             f'color: black;">{data_cert.get(
                                                                                 'name')}</span>')

                # Muestra el contenido del archivo en Streamlit con el texto resaltado
                st.markdown(f'<div style="height: 500px; overflow: auto;">{highlighted_content}</div>',
                            unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error al abrir el archivo: {e}")

        elif data_type == 'IMG':
            try:
                # Muestra la imagen en Streamlit
                st.image('app/' + path_file)
            except Exception as e:
                st.error(f"Error al abrir la imagen: {e}")


        elif data_type == 'DOC':
            with open('app/' + path_file, "rb") as f:
                pdf_data = f.read()

            # Convertir el archivo PDF a base64
            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')

            # Mostrar el PDF usando HTML
            st.markdown(f"""
                <iframe src="data:application/pdf;base64,{base64_pdf}" 
                        width="1100" height="1200" type="application/pdf"></iframe>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
