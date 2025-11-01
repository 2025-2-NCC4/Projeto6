# Home

import streamlit as st
from styles.footer import inject_footer
from styles.main import inject_global_styles
from styles.particles import inject_particles

# Configurações da página

st.set_page_config(
    page_title="Money BR",
    page_icon="assets/mbr_branco.png",
    layout="wide"
)

inject_global_styles()

# Principais

st.markdown("""
<style>        
.hero-section {
    position: relative;
    height: 600px; 
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: white;
    margin: 40px 60px 40px 60px;
    padding-top: 2rem;
    border-radius: 15px;
    overflow: hidden;
}

.hero-video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55));
}

.hero-content {
    position: relative;
    z-index: 1;
}
            
.hero-title {
    font-size: 55px !important;
    font-weight: bold;
    text-shadow: 2px 2px 8px #000000;
}
            
.hero-subtitle {
    font-size: 30px !important;
    text-shadow: 1px 1px 4px #000000;
}
            
.green-text {
    color: #007031;
}
            
</style>
""", unsafe_allow_html=True)

# Topo

st.markdown("""
<div class="hero-section">
    <video class="hero-video" autoplay muted loop playsinline poster="https://raw.githubusercontent.com/2025-2-NCC4/Projeto6/refs/heads/main/imagens/main-charts.mp4">
        <source src="https://raw.githubusercontent.com/2025-2-NCC4/Projeto6/refs/heads/main/imagens/main-charts.mp4" type="video/mp4">
    </video>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <h1 class="hero-title">MONEY <span class="green-text">BR</span></h1>
        <p class="hero-subtitle">Um conjunto de serviços essenciais para você!</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Seção de informações

st.markdown("""
<div class="info-section">
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title">Money BR: O amigo do seu bolso!</div>
            <div class="info-description">
            Nosso aplicativo é um divertido game de caça ao tesouro, em que os players procuram através de georreferencia e realidade aumentada por prêmios de real valor! Esses premios são cupons disponibilizados por lojistas através da nossa plataforma e são espalhados estrategicamente pela cidade, nas escolas e arredores, eventos culturais, clubes e associações esportivas.
            </div>
        </div>
        <div class="info-image-col">
            <img src="https://raw.githubusercontent.com/2025-2-NCC4/Projeto6/refs/heads/main/imagens/porquinho.jpg" style="width: 100%; border-radius: 10px;">
        </div>
    </div>
</div>

<style>
.info-section {
    margin: 40px 60px 40px 60px;
}

.info-content-wrapper {
    display: flex;
    gap: 2rem;
    align-items: flex-start;
}

.info-text-col {
    flex: 2;
}

.info-image-col {
    flex: 1;
    filter: brightness(0.6);
}
            
.info-title {
    color: #007031; 
    margin-bottom: 1.5rem;
    font-size: 40px;
    font-family: Inter;
    font-weight: bold;
}
            
.info-description {
    font-family: Inter;
    font-size: 25px;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

# Cards

st.markdown("""
<div class="cards-section">
    <div class="main-title">Encontre ofertas incríveis!</div>
    <div class="cards-wrapper">
        <div class="card-col">
            <img src="https://raw.githubusercontent.com/2025-2-NCC4/Projeto6/refs/heads/main/imagens/clothes.jpg">
            <div class='card-container'>
                <div class='card-content'>
                    <h3 class='card-title'>Cupons de desconto em roupas</h3>
                    <p class='card-text'>A Money BR renova seu guarda-roupa! Cupons de roupas te dão descontos incríveis nas lojas. Se está pensando em dar uma repaginada no seu visual, a hora é agora.</p>
                </div>
            </div>
        </div>
        <div class="card-col">
            <img src="https://raw.githubusercontent.com/2025-2-NCC4/Projeto6/refs/heads/main/imagens/green-food.jpg">
            <div class='card-container'>
                <div class='card-content'>
                    <h3 class='card-title'>Cupons de desconto em comida</h3>
                    <p class='card-text'>A Money BR também alimenta suas economias! Cupons de comida com descontos em restaurantes, lanchonetes e delivery. Se está com fome de economia, resgate o seu cupom!</p>
                </div>
            </div>
        </div>
        <div class="card-col">
            <img src="https://raw.githubusercontent.com/2025-2-NCC4/Projeto6/refs/heads/main/imagens/computer.jpg">
            <div class='card-container'>
                <div class='card-content'>
                    <h3 class='card-title'>Cupons de desconto em eletrônicos</h3>
                    <p class='card-text'>Está pensando em fazer um upgrade? A Money BR é parceira de muitas lojas de eletrônicos do Brasil. Use os cupons e garanta seu novo celular, notebook ou TV pagando muito menos.</p>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
            
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

.main-title {
    color: #007031; 
    margin-bottom: 1.5rem;
    font-size: 40px;
    font-family: Inter;
    font-weight: bold;
}

.cards-section {
    margin: 40px 60px 40px 60px;
}

.cards-wrapper {
    display: flex;
    gap: 1.5rem;
}

.card-col {
    flex: 1; 
}
            
.card-col img {
    width: 100%;
    height: 350px;
    object-fit: cover;
    filter: brightness(0.6);
    border-radius: 15px;
    margin-bottom: 30px;
}
            
.card-container {
    border: 3px solid #007031;
    border-radius: 15px; 
    overflow: hidden; 
    background-color: #1a1a1a; 
    padding: 0; 
    min-height: 100px;
    height: 43%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
            
.card-content {
    padding: 1.5rem;
    padding-top: 0;
    margin-top: 10px;
}
            
.card-content h3.card-title {
    font-family: Inter;
    font-size: 28px;
    font-weight: bold;
    color: #007031;
}
            
.card-content .card-text {
    font-family: Inter;
    font-size: 25px;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

# Partículas finais

inject_particles()

# Footer

inject_footer()