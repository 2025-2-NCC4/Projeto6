import streamlit as st
import requests
from streamlit_lottie import st_lottie
from styles.footer import inject_footer
from styles.main import inject_global_styles

# Configurações da página
st.set_page_config(
    page_title="Sobre",
    page_icon="💡",
    layout="wide"
)

inject_global_styles()

# Footer
inject_footer()