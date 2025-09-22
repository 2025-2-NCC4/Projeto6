import streamlit as st

def inject_global_styles():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    .stApp,
    [data-testid="stHeader"],
    [data-testid="stSidebar"],
    h1, h2, h3, h4, h5, h6, p {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #000000; 
    }
                
    [data-testid="stHeader"] {
        background-color: #000000;
    }
                
    .stApp > header, .stApp > [data-testid="stToolbar"] { display: none; }
    .block-container {
        padding: 0;
        margin: 0;
        max-width: 100vw;
        width: 100vw;
    }
                
    [data-testid="stSidebar"] {
        background-color: #000;
        color: white;
    }

    [data-testid="stSidebar"] a, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebarNav"] a, 
    [data-testid="stSidebarNav"] span {
        color: #fff !important;
        font-size: 30px !important;
    }

    [data-testid="stSidebarNav"] a {
        margin-left: 10px !important;
        margin-right: 10px !important;
        font-weight: bold;
        background-color: transparent !important;
        transition: background-color 0.3s ease;
    }

    /* Mouse */
    [data-testid="stSidebarNav"] a:hover {
        font-weight: bold;
        background-color: #007031 !important;
        transform: scale(1.1);
    }
                
    .main {
        padding: 0;
    }
    </style>
    """, unsafe_allow_html=True)