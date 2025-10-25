import streamlit as st

def inject_footer():
    
    st.markdown("""
    <div class="custom-footer">
        <div class="footer-top-bar"></div>
        <div class="footer-content">
            <div class="footer-title"><span class="footer-title-main">MONEY </span><span class="footer-title-green">BR</span></div>
            <div class="footer-menu">
                <a href="http://localhost:8501/" class="footer-link" target="_self">Home</a>
                <a href="http://localhost:8501/CEO" class="footer-link" target="_self">CEO</a>
                <a href="http://localhost:8501/CFO" class="footer-link" target="_self">CFO</a>
                <a href="http://localhost:8501/Sobre" class="footer-link" target="_self">Sobre</a>
            </div>
            <div class="footer-copy">Copyright © 2025 - 2025 <span class="footer-title-main">MONEY </span><span class="footer-title-green">BR</span></div>
        </div>
    </div>
    <style>
    .custom-footer {
        left: 0;
        bottom: 0;
        width: 100vw;
        background: #000;
        color: #fff;
        z-index: 9999;
        box-shadow: 0 -2px 8px rgba(0,0,0,0.15);
    }
    .footer-top-bar {
        width: 100vw;
        height: 5px;
        background: #007031;
        margin-bottom: 0.5rem;
    }
    .footer-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-bottom: 0.5rem;
    }
    .footer-title {
        font-size: 30px;
        font-family: Inter, sans-serif;
        font-weight: bold;
        margin-bottom: 1.2rem;
        letter-spacing: 2px;
    }
    .footer-title-main {
        color: #fff;
    }
    .footer-title-green {
        color: #007031;
    }
    .footer-menu {
        display: flex;
        gap: 3.5rem;
        margin-bottom: 1.2rem;
        flex-wrap: wrap;
    }
    .footer-link {
        color: #fff !important;
        text-decoration: none !important;
        font-size: 20px;
        font-family: Inter, sans-serif;
        font-weight: bold;
        transition: color 0.2s;
    }
    .footer-link:hover {
        color: #007031 !important;
        transform: scale(1.5);
        text-decoration: none !important;
    }
    .footer-copy {
        margin-top: 0.5rem;
        font-size: 15px;
        font-family: Inter, sans-serif;
        font-weight: bold;
    }
    @media (max-width: 900px) {
        .footer-menu { gap: 1.2rem; font-size: 1.1rem; }
        .footer-title { font-size: 2rem; }
    }
    </style>
    """, unsafe_allow_html=True)