import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os
import tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from styles.footer import inject_footer
from styles.main import inject_global_styles
from styles.particles import inject_particles
from Backend.pdf_builder import build_ceo_pdf
import base64

# Configurações da página

st.set_page_config(
    page_title="CEO",
    page_icon="assets/ceo-icon.png",
    layout="wide"
)

inject_global_styles()

inject_particles()

# Leitura de dados com cache

def load_csv(path: str, sep: str = ';', encoding: str = 'MacRoman', **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, sep=sep, encoding=encoding, **kwargs)

# Seção de informações

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            
<div class="info-section">
    <div class="info-content-wrapper">
        <div class="info-left-col">
            <div class="info-title-main"><i class="fa-solid fa-briefcase"></i> Painel executivo: Chief Executive Officer - CEO</div>
            <div class="info-description">
                O painel do CEO oferece uma visão abrangente do desempenho da empresa, destacando métricas essenciais do público, parceiros e performance geral da companhia. Com gráficos interativos e análises detalhadas, o CEO pode monitorar a saúde financeira da organização, identificar tendências de mercado e tomar decisões estratégicas informadas para impulsionar o sucesso a longo prazo.
                <br>
                <br>
                <span class="explore-sections-title">Explore as seções!</span>
            </div>
            <div class="navigation-bar">
                <a href="#volumetrias-gerais" class="nav-button">
                    <i class="fa-solid fa-chart-simple"></i> Volumetria geral
                </a>
                <a href="#dados-demograficos" class="nav-button">
                    <i class="fa-solid fa-map-location-dot"></i> Dados demográficos
                </a>
                <a href="#perfil-dos-clientes" class="nav-button">
                    <i class="fa-solid fa-user"></i> Perfil dos clientes
                </a>
                <a href="#detalhamento-avenida-paulista" class="nav-button">
                    <i class="fa-solid fa-road"></i> Detalhamento: Avenida Paulista
                </a>
                <a href="#relatorio-pdf" class="nav-button">
                    <i class="fa-solid fa-file-pdf"></i> Relatório em PDF
                </a>
            </div>
            <div class="info-description">
                <br>
                <span class="explore-sections-title">Visão financeira:</span>
            </div>
            <div class="navigation-bar">
                <a href="/CFO" class="nav-button">
                    <i class="fa-solid fa-money-bill-trend-up"></i> Painel CFO
                </a>
            </div>
        </div>

<div class="info-right-col">
            <img src="https://raw.githubusercontent.com/2025-2-NCC4/Projeto6/refs/heads/main/imagens/charts-ceo.jpg" style="width: 100%; border-radius: 10px;">
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

.info-left-col {
    flex: 2;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.info-right-col {
    flex: 1;
}

.info-title-main {
    color: #007031; 
    margin-bottom: 20px;
    font-size: 40px;
    font-family: Inter;
    font-weight: bold;
}

.info-description {
    font-family: Inter;
    font-size: 25px;
    color: #fff;
    margin-bottom: 20px;
}

.navigation-bar {
    display: flex;
    gap: 1rem;
}

.nav-button,
.nav-button:link,
.nav-button:visited {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    font-size: 20px;
    font-weight: 600;
    color: #ffffff !important;
    background-color: #007031;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    text-align: center;
    text-decoration: none !important;
    transition: background-color 0.3s ease;
}

.nav-button i {
    margin-right: 0.5rem;
}

.nav-button:hover {
    background-color: #005824;
}

.nav-button:active {
    background-color: #00471a;
}
            
.bar {
    width: 100vw !important;
    margin-left: -60px !important;
    margin-bottom: 50px !important;
    height: 5px;
    background: #007031;
}
</style>
""", unsafe_allow_html=True)

# Estilos dos filtros

st.markdown(
        """
<style>
.filter-toolbar { margin: 10px 60px 10px 60px; }
.filter-title { color: #FFF; font-family: Inter; font-size: 20px; font-weight: 700; margin-bottom: 6px; display:flex; gap:8px; align-items:center; }
.filter-title i { color:#fff; }

[data-testid="stMultiSelect"] {
    margin: 0 60px 30px 60px;
    background: #101414;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 10px 12px 2px 12px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.18);
}
[data-testid="stMultiSelect"] label { color:#AAB3C0; font-family: Inter; font-size: 13px; font-weight: 600; }
[data-testid="stMultiSelect"] div[data-baseweb="select"] { background: transparent; }
[data-testid="stMultiSelect"] div[data-baseweb="select"]>div { background: transparent; border:none; }
[data-testid="stMultiSelect"] input { color:#fff; font-family: Inter; }
[data-testid="stMultiSelect"] input::placeholder { color:#7c8794; }
[data-testid="stMultiSelect"] span { color:#fff; }
[data-baseweb="tag"] { background:#007031; color:#fff; border-radius:8px; font-family: Inter; }
[data-testid="stMultiSelect"] div[data-baseweb="select"]:focus-within { box-shadow: 0 0 0 2px rgba(0,112,49,0.45); border-radius:10px; }
</style>
""",
        unsafe_allow_html=True,
)

# Volumetrias gerais

st.markdown("""
<div class="info-section">
    <div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div id="volumetrias-gerais" class="info-title"><i class="fa-solid fa-chart-simple"></i> Volumetrias gerais</div>
        </div>
    </div>
</div>
<div class="filter-toolbar">
    <div class="filter-title"><i class="fa-solid fa-sliders"></i> Aplicar filtros</div>
</div>
<style>
.info-title {
    color: #007031;
    font-size: 30px;
    font-family: Inter;
    font-weight: bold;
}
            
.fa-solid {
    color: #fff;
}
            
</style>
""", unsafe_allow_html=True)

try:
    df = load_csv("data/Base_de_Transacoes_Cupons_Capturados.csv", sep=';', encoding='MacRoman')

    if not df.empty:
        # Filtros

        col_filtros_1, col_filtros_2, col_filtros_3 = st.columns(3)

        # Filtro Estabelecimentos
        with col_filtros_1:
            estabelecimentos_unicos = df['nome_estabelecimento'].unique()
            estabelecimentos_selecionados = st.multiselect(
                "Filtre por estabelecimento:",
                options=sorted(estabelecimentos_unicos),
                default=[], 
                placeholder="Selecione um ou mais estabelecimentos"
            )

        # Filtro Categorias
        with col_filtros_2:
            categorias_unicas = df['categoria_estabelecimento'].unique()
            categorias_selecionadas = st.multiselect(
                "Filtre por categoria:",
                options=sorted(categorias_unicas),
                default=[],
                placeholder="Selecione uma ou mais categorias"
            )

        # Filtro Bairros
        with col_filtros_3:
            bairros_unicos = df['bairro_estabelecimento'].unique()
            bairros_selecionados = st.multiselect(
                "Filtre por bairro:",
                options=sorted(bairros_unicos),
                default=[],
                placeholder="Selecione um ou mais bairros"
            )

        df_filtrado = df.copy() # Cópia de df

        # Filtros em cascata
        if estabelecimentos_selecionados:
            df_filtrado = df_filtrado[df_filtrado['nome_estabelecimento'].isin(estabelecimentos_selecionados)]
            
        if categorias_selecionadas:
            df_filtrado = df_filtrado[df_filtrado['categoria_estabelecimento'].isin(categorias_selecionadas)]
            
        if bairros_selecionados:
            df_filtrado = df_filtrado[df_filtrado['bairro_estabelecimento'].isin(bairros_selecionados)]

        # Verificar se há dados
        if not df_filtrado.empty:
            # Top 10 estabelecimentos
            top_10_estabelecimentos = df_filtrado['nome_estabelecimento'].value_counts().head(10)
            df_top_10_estab = pd.DataFrame({
                'Estabelecimento': top_10_estabelecimentos.index,
                'Número de transações': top_10_estabelecimentos.values
            })

            fig_estab = px.bar(
                df_top_10_estab,
                x='Número de transações',
                y='Estabelecimento',
                title=f"Top {len(df_top_10_estab)} estabelecimentos por número de transações (Filtrado)",
                orientation='h',
                color='Número de transações',
                color_continuous_scale=[
                '#e5f5e0',  # verde bem claro
                '#a1d99b',  # verde claro
                '#74c476',  # verde médio
                '#31a354',  # verde forte
                '#006d2c'   # verde escuro
            ],
                text='Número de transações'
            )

            fig_estab.update_layout(
                title=dict(text=f"Top {len(df_top_10_estab)} estabelecimento(s) por número de transações", font=dict(size=22), x=0.05),
                yaxis_title=dict(text="Estabelecimento", font=dict(size=22)),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16)),
                legend=dict(font=dict(size=14)),
                legend_title=dict(font=dict(size=16)),
            )

            fig_estab.update_traces(
                texttemplate='%{text:,}',
                textposition='inside',
                textfont_size=16
            )

            # --- Top 10 categorias ---
            top_10_categorias = df_filtrado['categoria_estabelecimento'].value_counts().head(10)
            df_top_10_cat = pd.DataFrame({
                'Categoria': top_10_categorias.index,
                'Número de transações': top_10_categorias.values
            })

            fig_cat = px.bar(
                df_top_10_cat,
                x='Número de transações',
                y='Categoria',
                title=f"Top {len(df_top_10_cat)} categorias por número de transações (Filtrado)",
                color='Número de transações',
                color_continuous_scale=[
                '#e5f5e0',  
                '#a1d99b', 
                '#74c476',  
                '#31a354', 
                '#006d2c'   
            ],
                text='Número de transações'
            )

            fig_cat.update_layout(
                title=dict(text=f"Top {len(df_top_10_cat)} categoria(s) por número de transações", font=dict(size=22), x=0.05),
                xaxis_title=dict(text="Número de transações", font=dict(size=22)),
                yaxis_title=dict(text="Categoria", font=dict(size=22)),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16)),
                legend=dict(font=dict(size=14)),
                legend_title=dict(font=dict(size=16))
            )

            fig_cat.update_traces(
                texttemplate='%{text:,}',
                textposition='inside',
                textfont_size=16
            )

            _left_gutter, col1, col2, _right_gutter = st.columns([0.03, 0.47, 0.47, 0.03])
            with col1:
                st.plotly_chart(fig_estab, use_container_width=True, key="grafico_estabelecimentos")
            with col2:
                st.plotly_chart(fig_cat, use_container_width=True, key="grafico_categorias")

            # --- Top 10 bairros ---
            top_10_bairros = df_filtrado['bairro_estabelecimento'].value_counts().head(10)
            df_top_10_bairros = pd.DataFrame({
                'Bairro': top_10_bairros.index,
                'Número de transações': top_10_bairros.values
            })
            fig_bairros = px.bar(
                df_top_10_bairros,
                x='Número de transações',
                y='Bairro',
                title=f"Top {len(df_top_10_bairros)} bairros por número de transações (Filtrado)",
                orientation='h',
                color='Número de transações',
                color_continuous_scale=[
                    '#e5f5e0', '#a1d99b', '#74c476', '#31a354', '#006d2c'
                ],
                text='Número de transações'
            )
            fig_bairros.update_layout(
                title=dict(text=f"Top {len(df_top_10_bairros)} bairro(s) por número de transações", font=dict(size=22), x=0.05),
                xaxis_title=dict(text="Número de transações", font=dict(size=22)),
                yaxis_title=dict(text="Bairro", font=dict(size=22)),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16)),
                legend=dict(font=dict(size=14)),
                legend_title=dict(font=dict(size=16))
            )
            fig_bairros.update_traces(
                texttemplate='%{text:,}',
                textposition='inside',
                textfont_size=16
            )

            # --- Cupons ---
            top_10_cupons = df_filtrado['tipo_cupom'].value_counts().head(10)
            df_top_10_cupons = pd.DataFrame({
                'Tipo de cupom': top_10_cupons.index,
                'Número de transações': top_10_cupons.values
            })
            fig_cupons = px.bar(
                df_top_10_cupons,
                x='Número de transações',
                y='Tipo de cupom',
                title="Quantidade de cupons por transações",
                orientation='h',
                color='Número de transações',
                color_continuous_scale=[
                    '#e5f5e0', '#a1d99b', '#74c476', '#31a354', '#006d2c'
                ],
                text='Número de transações'
            )
            fig_cupons.update_layout(
                title=dict(text="Quantidade de cupons por transações", font=dict(size=22), x=0.05),
                xaxis_title=dict(text="Número de transações", font=dict(size=22)),
                yaxis_title=dict(text="Tipo de cupom", font=dict(size=22)),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16)),
                legend=dict(font=dict(size=14)),
                legend_title=dict(font=dict(size=16))
            )
            fig_cupons.update_traces(
                texttemplate='%{text:,}',
                textposition='inside',
                textfont_size=16
            )

            # --- Mostrar os dois novos gráficos lado a lado ---
            _left_gutter2, col3, col4, _right_gutter2 = st.columns([0.03, 0.47, 0.47, 0.03])
            with col3:
                st.plotly_chart(fig_bairros, use_container_width=True, key="grafico_bairros")
            with col4:
                st.plotly_chart(fig_cupons, use_container_width=True, key="grafico_cupons")
        else:
            st.info("Não há transações para a combinação de filtros selecionada. Tente reduzir o número de filtros.")
except FileNotFoundError:
    st.error("Erro: O arquivo 'Base_de_Transacoes_Cupons_Capturados.csv' não foi encontrado.")
    st.info("Por favor, verifique se o arquivo está na pasta correta.")
except KeyError as e:
    st.error(f"Erro: A coluna {e} não foi encontrada. Verifique se o nome da coluna no seu arquivo .CSV está correto.")
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")

# Dados demográficos

st.markdown("""
<div id="dados-demograficos" class="info-section">
    <div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-map-location-dot"></i> Dados demográficos</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

try:

     df_demo = load_csv("data/Base_Cadastral_de_Players.csv", sep=';', encoding='MacRoman')

     if not df_demo.empty:
        # Filtros

        col_filtros_1, col_filtros_2, col_filtros_3, col_filtros_4 = st.columns(4)

        # Filtro cidade residencial
        with col_filtros_1:
            cidade_res_unicos = df_demo['cidade_residencial'].unique()
            cidade_res_selecionadas = st.multiselect(
                "Filtre por cidade residencial:",
                options=sorted(cidade_res_unicos),
                default=[], 
                placeholder="Selecione uma ou mais cidades"
            )

        # Filtro bairro residencial
        with col_filtros_2:
            bairro_res_unicos = df_demo['bairro_residencial'].unique()
            bairro_res_selecionados = st.multiselect(
                "Filtre por bairro residencial:",
                options=sorted(bairro_res_unicos),
                default=[],
                placeholder="Selecione um ou mais bairros residenciais"
            )

        # Filtro cidade de trabalho
        with col_filtros_3:
            cidade_trab_unicos = df_demo['cidade_trabalho'].unique()
            cidade_trab_selecionadas = st.multiselect(
                "Filtre por cidade de trabalho:",
                options=sorted(cidade_trab_unicos),
                default=[],
                placeholder="Selecione uma ou mais cidades de trabalho"
            )

        # Filtro bairro de trabalho
        with col_filtros_4:
            bairro_trab_unicos = df_demo['bairro_trabalho'].unique()
            bairro_trab_selecionados = st.multiselect(
                "Filtre por bairro de trabalho:",
                options=sorted(bairro_trab_unicos),
                default=[],
                placeholder="Selecione um ou mais bairros de trabalho"
            )

        df_filtrado_demo = df_demo.copy() # Cópia de df

        # Filtros em cascata
        if cidade_res_selecionadas:
            df_filtrado_demo = df_filtrado_demo[df_filtrado_demo['cidade_residencial'].isin(cidade_res_selecionadas)]
            
        if bairro_res_selecionados:
            df_filtrado_demo = df_filtrado_demo[df_filtrado_demo['bairro_residencial'].isin(bairro_res_selecionados)]

        if bairro_res_selecionados:
            df_filtrado_demo = df_filtrado_demo[df_filtrado_demo['bairro_residencial'].isin(bairro_res_selecionados)]

        if cidade_trab_selecionadas:
            df_filtrado_demo = df_filtrado_demo[df_filtrado_demo['cidade_trabalho'].isin(cidade_trab_selecionadas)]

        if bairro_trab_selecionados:
            df_filtrado_demo = df_filtrado_demo[df_filtrado_demo['bairro_trabalho'].isin(bairro_trab_selecionados)]

        # Verificar se há dados
        if not df_filtrado_demo.empty:
            # --- Cidade Residencial ---
            cidade_res_counts = df_filtrado_demo['cidade_residencial'].value_counts().reset_index().head(10)
            cidade_res_counts.columns = ['Cidade Residencial', 'Quantidade']

            fig_cidade_res = px.bar(
                cidade_res_counts,
                x='Quantidade',
                y='Cidade Residencial',
                orientation='h',
                text='Quantidade',
                title="10 maiores quantidades de usuários por cidade residencial",
                color='Quantidade',
                color_continuous_scale=['#e5f5e0','#a1d99b','#74c476','#31a354','#006d2c']
            )
            fig_cidade_res.update_layout(
                title=dict(text="10 maiores quantidades de usuários por cidade residencial", font=dict(size=22), x=0.05),
                xaxis_title=dict(text="Quantidade de usuários", font=dict(size=22)),
                yaxis_title=dict(text="Cidade Residencial", font=dict(size=22)),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16)),
                showlegend=False
            )
            fig_cidade_res.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                textfont_size=16
            )

            # --- Bairro Residencial ---
            bairro_res_counts = df_filtrado_demo['bairro_residencial'].value_counts().reset_index().head(10)
            bairro_res_counts.columns = ['Bairro Residencial', 'Quantidade']

            fig_bairro_res = px.bar(
                bairro_res_counts,
                x='Quantidade',
                y='Bairro Residencial',
                orientation='h',
                text='Quantidade',
                title="10 maiores quantidades de usuários por bairro residencial",
                color='Quantidade',
                color_continuous_scale=['#e5f5e0','#a1d99b','#74c476','#31a354','#006d2c']
            )
            fig_bairro_res.update_layout(
                title=dict(text="10 maiores quantidades de usuários por bairro residencial", font=dict(size=22), x=0.05),
                xaxis_title=dict(text="Quantidade de usuários", font=dict(size=22)),
                yaxis_title=dict(text="Bairro Residencial", font=dict(size=22)),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16)),
                showlegend=False
            )
            fig_bairro_res.update_traces(
                texttemplate='%{text:,}',
                textposition='inside',
                textfont_size=16
            )

            # --- Cidade Trabalho ---
            cidade_trab_counts = df_filtrado_demo['cidade_trabalho'].value_counts().reset_index()
            cidade_trab_counts.columns = ['Cidade Trabalho', 'Quantidade']

            fig_cidade_trab = px.bar(
                cidade_trab_counts,
                x='Quantidade',
                y='Cidade Trabalho',
                orientation='h',
                text='Quantidade',
                title="Quantidade de usuários por cidade de trabalho",
                color='Quantidade',
                color_continuous_scale=['#e5f5e0','#a1d99b','#74c476','#31a354','#006d2c']
            )
            fig_cidade_trab.update_layout(
                title=dict(text="Quantidade de usuários por cidade de trabalho", font=dict(size=22), x=0.05),
                xaxis_title=dict(text="Quantidade de usuários", font=dict(size=22)),
                yaxis_title=dict(text="Cidade de Trabalho", font=dict(size=22)),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16)),
                showlegend=False
            )
            fig_cidade_trab.update_traces(
                texttemplate='%{text:,}',
                textposition='inside',
                textfont_size=16
            )

            # --- Bairro Trabalho ---
            bairro_trab_counts = df_filtrado_demo['bairro_trabalho'].value_counts().reset_index().head(10)
            bairro_trab_counts.columns = ['Bairro Trabalho', 'Quantidade']

            fig_bairro_trab = px.bar(
                bairro_trab_counts,
                x='Quantidade',
                y='Bairro Trabalho',
                orientation='h',
                text='Quantidade',
                title="10 maiores quantidades de usuários por bairro de trabalho",
                color='Quantidade',
                color_continuous_scale=['#e5f5e0','#a1d99b','#74c476','#31a354','#006d2c']
            )
            fig_bairro_trab.update_layout(
                title=dict(text="10 maiores quantidades de usuários por bairro de trabalho", font=dict(size=22), x=0.05),
                xaxis_title=dict(text="Quantidade de usuários", font=dict(size=22)),
                yaxis_title=dict(text="Bairro de Trabalho", font=dict(size=22)),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16)),
                showlegend=False,
            )
            fig_bairro_trab.update_traces(
                texttemplate='%{text:,}',
                textposition='inside',
                textfont_size=16
            )

            # --- Mostrar gráficos ---
            _left_gutter6, col1, col2, _right_gutter6 = st.columns([0.03, 0.47, 0.47, 0.03])
            with col1:
                st.plotly_chart(fig_cidade_res, use_container_width=True, key="grafico_cidade_res")
            with col2:
                st.plotly_chart(fig_bairro_res, use_container_width=True, key="grafico_bairro_res")

            _left_gutter7, col3, col4, _right_gutter7 = st.columns([0.03, 0.47, 0.47, 0.03])
            with col3:
                st.plotly_chart(fig_cidade_trab, use_container_width=True, key="grafico_cidade_trab")
            with col4:
                st.plotly_chart(fig_bairro_trab, use_container_width=True, key="grafico_bairro_trab")
        else:
            st.info("Não há dados para a combinação de filtros selecionada.")
except FileNotFoundError:
    st.error("Erro: O arquivo 'Base_Cadastral_de_Players.csv' não foi encontrado.")
except KeyError as e:
    st.error(f"Erro: A coluna {e} não foi encontrada. Verifique o nome no CSV.")
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")

# Perfil dos clientes e avenida paulista

st.markdown("""
<div id="perfil-dos-clientes" class="info-section">
<div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-user"></i> Perfil dos clientes</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

try:
    df_paulista = load_csv("data/Base_Simulada_Pedestres_Av_Paulista.csv", sep=';', encoding='MacRoman')

    if not df_paulista.empty:
        # Histograma: Idade

        nbins = 10
        df_paulista['faixa_idade'] = pd.cut(df_paulista['idade'], bins=nbins)

        grouped = df_paulista['faixa_idade'].value_counts().sort_index().reset_index()
        grouped.columns = ['faixa_idade', 'Quantidade']

        def fmt_interval(iv):
            l = int(np.floor(iv.left))
            r = int(np.ceil(iv.right))
            return f"{l}–{r}"

        # Formatação compacta de moeda

        def _fmt_currency_compact_br(value: float) -> str:
            try:
                v = float(value) if value is not None else 0.0
            except Exception:
                v = 0.0
            av = abs(v)
            if av >= 1_000_000_000:
                s = f"{v/1_000_000_000:.1f}".replace(".", ",")
                return f"R$ {s} bi"
            if av >= 1_000_000:
                s = f"{v/1_000_000:.1f}".replace(".", ",")
                return f"R$ {s} mi"
            if av >= 1_000:
                s = f"{v/1_000:.1f}".replace(".", ",")
                return f"R$ {s} mil"
            txt = f"{v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return f"R$ {txt}"

        grouped['faixa'] = grouped['faixa_idade'].apply(fmt_interval)
        grouped = grouped.sort_values('faixa_idade')
        grouped['faixa'] = pd.Categorical(grouped['faixa'], categories=grouped['faixa'], ordered=True)

        fig_idade = px.bar(
            grouped,
            x='faixa',
            y='Quantidade',
            text='Quantidade',
            title="Distribuição de idade dos usuários",
            color='Quantidade', 
            color_continuous_scale=[
                '#e5f5e0', '#a1d99b', '#74c476', '#31a354', '#006d2c'
            ],
        )

        fig_idade.update_layout(
            title=dict(text="Distribuição de idade dos usuários", font=dict(size=22), x=0.05),
            xaxis_title=dict(text="Faixa de idade", font=dict(size=22)),
            yaxis_title=dict(text="Quantidade de usuários", font=dict(size=22)),
            xaxis=dict(tickfont=dict(size=16)),
            yaxis=dict(tickfont=dict(size=16)),
            bargap=0.05,
            showlegend=False
        )

        fig_idade.update_traces(
            marker_line_color="black",
            marker_line_width=0.5,
            texttemplate='%{text:,}',
            textposition='inside',
            textfont_size=16
        )

        fig_idade.update_xaxes(tickangle=0, tickfont=dict(size=15))

        # Montante gasto por faixa de idade

        gasto_por_faixa = df_paulista.groupby('faixa_idade')['ultimo_valor_capturado'].sum().reset_index()
        gasto_por_faixa['faixa'] = gasto_por_faixa['faixa_idade'].apply(fmt_interval)
        gasto_por_faixa = gasto_por_faixa.sort_values('faixa_idade')

        # Rótulos compactos para caber nas barras

        gasto_por_faixa['label_br'] = gasto_por_faixa['ultimo_valor_capturado'].apply(_fmt_currency_compact_br)

        fig_gasto = px.bar(
            gasto_por_faixa,
            x='faixa',
            y='ultimo_valor_capturado',
            text='label_br',
            title="Montante gasto por faixa de idade",
            color='ultimo_valor_capturado',
            color_continuous_scale=['#e5f5e0','#a1d99b','#74c476','#31a354','#006d2c']
        )

        fig_gasto.update_layout(
            title=dict(text="Montante gasto por faixa de idade", font=dict(size=22), x=0.05),
            xaxis_title=dict(text="Faixa de idade", font=dict(size=22)),
            yaxis_title=dict(text="Montante gasto", font=dict(size=22)),
            xaxis=dict(tickfont=dict(size=16)),
            yaxis=dict(tickfont=dict(size=16)),
            coloraxis_colorbar=dict(title="Montante gasto"),
            bargap=0.05,
        )

        fig_gasto.update_traces(texttemplate='%{text}', textposition='inside', textfont_size=16)
        fig_gasto.update_yaxes(tickprefix='R$ ')

        fig_gasto.update_xaxes(tickangle=0, tickfont=dict(size=15))

        # Gráfico de rosca: Sexo

        sexo_counts = df_paulista['sexo'].value_counts().reset_index()
        sexo_counts.columns = ["Sexo", "Quantidade"]

        fig_sexo = px.pie(
            sexo_counts,
            values="Quantidade",
            names="Sexo",
            title="Proporção de usuários por sexo",
            hole=0.5,
            color_discrete_sequence=["#74c476", "#006d2c"]
        )

        fig_sexo.update_traces(
            textinfo="percent+label+value", textfont_size=14
        )

        fig_sexo.update_layout(
        title=dict(text="Proporção de usuários por sexo", font=dict(size=22), x=0.05),
        legend_title=dict(font=dict(size=18)),
            legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        )
        )

        # Modelo de celular

        modelo_counts = df_paulista['modelo_celular'].value_counts().reset_index()
        modelo_counts.columns = ['Modelo de Celular', 'Quantidade']

        fig_modelo = px.bar(
            modelo_counts,
            x='Quantidade',
            y='Modelo de Celular',
            orientation='h',
            text='Quantidade',
            title="Quantidade de usuários por modelo de celular",
            color='Quantidade',
            color_continuous_scale=['#e5f5e0','#a1d99b','#74c476','#31a354','#006d2c']
        )

        fig_modelo.update_layout(
            title=dict(text="Quantidade de usuários por modelo de celular", font=dict(size=22), x=0.05),
            xaxis_title=dict(text="Quantidade de usuários", font=dict(size=22)),
            yaxis_title=dict(text="Modelo de Celular", font=dict(size=22)),
            xaxis=dict(tickfont=dict(size=16)),
            yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16)),
            showlegend=False
        )

        fig_modelo.update_traces(
            texttemplate='%{text:,}',
            textposition='inside',
            textfont_size=16
        )

        # Faixa de horários

        df_paulista['horario'] = pd.to_datetime(df_paulista['horario'], format='%H:%M:%S', errors='coerce').dt.time

        def faixa_horario(h):
            if h >= pd.to_datetime('00:00:00').time() and h <= pd.to_datetime('11:59:59').time():
                return 'Manhã'
            elif h >= pd.to_datetime('12:00:00').time() and h <= pd.to_datetime('18:59:59').time():
                return 'Tarde'
            else:
                return 'Noite'

        df_paulista['faixa_horario'] = df_paulista['horario'].apply(faixa_horario)

        horario_counts = df_paulista['faixa_horario'].value_counts().reindex(['Manhã','Tarde','Noite']).reset_index()
        horario_counts.columns = ['Faixa de Horário', 'Quantidade']

        fig_horario = px.bar(
            horario_counts,
            x='Faixa de Horário',
            y='Quantidade',
            text='Quantidade',
            title="Distribuição de registros por faixa de horário",
            color='Quantidade',
            color_continuous_scale=['#e5f5e0','#a1d99b','#74c476','#31a354','#006d2c']
        )

        fig_horario.update_layout(
            title=dict(text="Distribuição de registros por faixa de horário", font=dict(size=22), x=0.05),
            xaxis_title=dict(text="Faixa de horário", font=dict(size=22)),
            yaxis_title=dict(text="Quantidade de registros", font=dict(size=22)),
            xaxis=dict(tickfont=dict(size=16)),
            yaxis=dict(tickfont=dict(size=16)),
            bargap=0.1,
            showlegend=False
        )

        fig_horario.update_traces(
            marker_line_color="black",
            marker_line_width=0.5,
            texttemplate='%{text:,}',
            textposition='inside',
            textfont_size=16
        )

        # Principais locais

        top_locais = df_paulista['local'].value_counts().head(10).reset_index()
        top_locais.columns = ['Local', 'Quantidade']

        fig_local = px.bar(
            top_locais,
            x='Quantidade',
            y='Local',
            text='Quantidade',
            orientation='h',
            title="Top 10 locais com mais registros",
            color='Quantidade',
            color_continuous_scale=['#e5f5e0','#a1d99b','#74c476','#31a354','#006d2c']
        )

        fig_local.update_layout(
            title=dict(text="Top 10 locais com mais registros", font=dict(size=22), x=0.05),
            xaxis_title=dict(text="Quantidade de registros", font=dict(size=22)),
            yaxis_title=dict(text="Local", font=dict(size=22)),
            xaxis=dict(tickfont=dict(size=16)),
            yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16)),
            showlegend=False
        )

        fig_local.update_traces(
            texttemplate='%{text:,}',
            textposition='inside',
            textfont_size=16
        )

        # Mostrar lado a lado

        _left_gutter3, col1, col2, _right_gutter3 = st.columns([0.03, 0.47, 0.47, 0.03])
        with col1:
            st.plotly_chart(fig_idade, use_container_width=True, key="grafico_idade")
        with col2:
            st.plotly_chart(fig_gasto, use_container_width=True, key="grafico_gasto")

        _left_gutter4, col3, col4, _right_gutter4 = st.columns([0.03, 0.47, 0.47, 0.03])
        with col3:
            st.plotly_chart(fig_sexo, use_container_width=True, key="grafico_sexo")
        with col4:
            st.plotly_chart(fig_modelo, use_container_width=True, key="grafico_modelo")

        st.markdown("""
        <div id="detalhamento-avenida-paulista" class="info-section">
            <div class="bar"></div>
            <div class="info-content-wrapper">
                <div class="info-text-col">
                    <div class="info-title"><i class="fa-solid fa-road"></i> Detalhamento: Avenida Paulista</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        _left_gutter5, col5, col6, _right_gutter5 = st.columns([0.03, 0.47, 0.47, 0.03])
        with col5:
            st.plotly_chart(fig_horario, use_container_width=True, key="grafico_horario")
        with col6:
            st.plotly_chart(fig_local, use_container_width=True, key="grafico_local")     
    else:
        st.info("O arquivo 'Base_Simulada_Pedestres_Av_Paulista.csv' está vazio.")
except FileNotFoundError:
    st.error("Erro: O arquivo 'Base_Simulada_Pedestres_Av_Paulista.csv' não foi encontrado.")
except KeyError as e:
    st.error(f"Erro: A coluna {e} não foi encontrada. Verifique o nome no CSV.")
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")

if 'charts' not in st.session_state:
    st.session_state.charts = {}

st.session_state.charts["fig_estab"] = fig_estab
st.session_state.charts["fig_cat"] = fig_cat
st.session_state.charts["fig_bairros"] = fig_bairros
st.session_state.charts["fig_cupons"] = fig_cupons
st.session_state.charts["fig_cidade_res"] = fig_cidade_res
st.session_state.charts["fig_bairro_res"] = fig_bairro_res
st.session_state.charts["fig_cidade_trab"] = fig_cidade_trab
st.session_state.charts["fig_bairro_trab"] = fig_bairro_trab
st.session_state.charts["fig_idade"] = fig_idade
st.session_state.charts["fig_gasto"] = fig_gasto
st.session_state.charts["fig_sexo"] = fig_sexo
st.session_state.charts["fig_modelo"] = fig_modelo
st.session_state.charts["fig_horario"] = fig_horario
st.session_state.charts["fig_local"] = fig_local

# Seção de Relatório em PDF
st.markdown("""
<div id="relatorio-pdf" class="info-section">
    <div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-file-pdf"></i> Relatório em PDF</div>
        </div>
    </div>
</div>
<div class="filter-toolbar">
    <div class="filter-title"><i class="fa-solid fa-circle-info"></i> Gere um relatório completo em PDF com todos os insights estratégicos baseado nos filtros que foram aplicados</div>
</div>
""", unsafe_allow_html=True)

# Estilização do botão para seguir o padrão do projeto
st.markdown("""
<style>
.pdf-button-container {
    margin: 0 60px 30px 60px;
}
.stButton > button {
    background-color: #007031 !important;
    border: none !important;
    border-radius: 0.5rem !important;
    padding: 0.65rem 1.25rem !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    color: #ffffff !important;
    transition: background-color 0.3s ease !important;
    width: auto !important;
    margin: 0 !important;
    display: inline-block !important;
    min-width: 250px !important;
}
.stButton > button:hover {
    background-color: #005824 !important;
    border: none !important;
}
.stButton > button:active {
    background-color: #00471a !important;
    border: none !important;
}
.stButton > button:focus {
    background-color: #007031 !important;
    border: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# Container para o botão alinhado à esquerda
st.markdown('<div class="pdf-button-container">', unsafe_allow_html=True)
if st.button("📄 Gerar Relatório em PDF"):
    st.write("Gerando PDF com insights estratégicos...")
    
    # Preparar filtros
    filtros = {
        'estabelecimentos': estabelecimentos_selecionados if estabelecimentos_selecionados else [],
        'categorias': categorias_selecionadas if categorias_selecionadas else [],
        'bairros': bairros_selecionados if bairros_selecionados else []
    }
    
    # Preparar dataframes
    dataframes = {
        'df_top_estabelecimentos': df_top_10_estab if 'df_top_10_estab' in locals() else pd.DataFrame(),
        'df_top_categorias': df_top_10_cat if 'df_top_10_cat' in locals() else pd.DataFrame(),
        'df_top_bairros': df_top_10_bairros if 'df_top_10_bairros' in locals() else pd.DataFrame(),
        'df_cupons': df_top_10_cupons if 'df_top_10_cupons' in locals() else pd.DataFrame(),
        'df_base': df_base if 'df_base' in locals() else pd.DataFrame(),
        'df_cidade_res': cidade_res_counts if 'cidade_res_counts' in locals() else pd.DataFrame(),
        'df_bairro_res': bairro_res_counts if 'bairro_res_counts' in locals() else pd.DataFrame(),
        'df_cidade_trab': cidade_trab_counts if 'cidade_trab_counts' in locals() else pd.DataFrame(),
        'df_bairro_trab': bairro_trab_counts if 'bairro_trab_counts' in locals() else pd.DataFrame(),
        'df_paulista': df_paulista if 'df_paulista' in locals() else pd.DataFrame()
    }
    
    # Salvar gráficos em arquivos temporários
    temp_dir = tempfile.mkdtemp(prefix='moneybr_charts_')
    
    chart_paths = {}
    charts_to_save = {
        "fig_estab": fig_estab,
        "fig_cat": fig_cat,
        "fig_bairros": fig_bairros,
        "fig_cupons": fig_cupons,
        "fig_cidade_res": fig_cidade_res,
        "fig_bairro_res": fig_bairro_res,
        "fig_cidade_trab": fig_cidade_trab,
        "fig_bairro_trab": fig_bairro_trab,
        "fig_idade": fig_idade,
        "fig_gasto": fig_gasto,
        "fig_sexo": fig_sexo,
        "fig_modelo": fig_modelo,
        "fig_horario": fig_horario,
        "fig_local": fig_local
    }
    
    for name, fig in charts_to_save.items():
        if fig is not None:
            chart_path = os.path.join(temp_dir, f"{name}.png")
            fig.write_image(chart_path)
            chart_paths[name] = chart_path
    
    # Gerar PDF com insights
    try:
        pdf_output = build_ceo_pdf(filtros, dataframes, chart_paths, temp_dir)
        b64 = base64.b64encode(pdf_output).decode('utf-8')
        
        # Link de download estilizado
        st.markdown(f"""
        <style>
        .download-container {{{{
            display: flex;
            justify-content: flex-start;
            margin: 30px 0;
        }}}}
        .download-link {{{{
            background: linear-gradient(135deg, #56ac37 0%, #007031 100%);
            color: white !important;
            padding: 14px 40px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            text-decoration: none;
            box-shadow: 0 4px 12px rgba(86, 172, 55, 0.3);
            transition: all 0.3s ease;
            display: inline-block;
        }}}}
        .download-link:hover {{{{
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(86, 172, 55, 0.4);
            text-decoration: none;
        }}}}
        </style>
        <div class="download-container">
            <a href="data:application/octet-stream;base64,{b64}" download="relatorio_ceo_completo.pdf" class="download-link">
                📥 Download do Relatório CEO
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("✅ PDF gerado com sucesso! Clique no botão acima para baixar.")
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
        import traceback
        st.code(traceback.format_exc())

st.markdown('</div>', unsafe_allow_html=True)

# Footer

inject_footer()