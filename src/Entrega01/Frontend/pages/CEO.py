import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
from styles.footer import inject_footer
from styles.main import inject_global_styles
from styles.particles import inject_particles  
 
# Configurações da página

st.set_page_config(
    page_title="CEO",
    page_icon="📊",
    layout="wide"
)

inject_global_styles()

inject_particles()

# Seção de informações

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            
<div class="info-section">
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-user-tie"></i> Painel executivo: Chief Executive Officer - CEO</div>
            <div class="info-description">
                O painel do CEO oferece uma visão abrangente do desempenho da empresa, destacando métricas essenciais do público, parceiros e performance geral da companhia. Com gráficos interativos e análises detalhadas, o CEO pode monitorar a saúde financeira da organização, identificar tendências de mercado e tomar decisões estratégicas informadas para impulsionar o sucesso a longo prazo.
            </div>
        </div>
        <div class="info-image-col">
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
            
.bar {
    width: 100vw !important;
    margin-left: -60px !important;
    margin-bottom: 50px !important;
    height: 5px;
    background: #007031;
}
            
.fa-solid {
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

# Volumetrias gerais

st.markdown("""
<div class="info-section">
    <div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-chart-simple"></i> Volumetrias gerais</div>
        </div>
    </div>
</div>
<style>
.info-title {
    color: #007031;
    font-size: 30px;
    font-family: Inter;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

try:
    df = pd.read_csv("data/Base_de_Transacoes_Cupons_Capturados.csv", sep=';', encoding='MacRoman')

    # --- Top 10 estabelecimentos ---
    top_10_estabelecimentos = df['nome_estabelecimento'].value_counts().head(10)
    df_top_10_estab = pd.DataFrame({
        'Estabelecimento': top_10_estabelecimentos.index,
        'Número de transações': top_10_estabelecimentos.values
    })

    fig_estab = px.bar(
        df_top_10_estab,
        x='Número de transações',
        y='Estabelecimento',
        title="Top 10 estabelecimentos por número de transações",
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
        title=dict(text="Top 10 estabelecimentos por número de transações", font=dict(size=22), x=0.05),
        xaxis_title=dict(text="Número de transações", font=dict(size=18)),
        yaxis_title=dict(text="Estabelecimento", font=dict(size=18)),
        yaxis={'categoryorder': 'total ascending'},
        legend=dict(font=dict(size=14)),
        legend_title=dict(font=dict(size=16)),
    )

    fig_estab.update_traces(
        texttemplate='%{text:,}',
        textposition='inside'
    )

    # --- Top 10 categorias ---
    top_10_categorias = df['categoria_estabelecimento'].value_counts().head(10)
    df_top_10_cat = pd.DataFrame({
        'Categoria': top_10_categorias.index,
        'Número de transações': top_10_categorias.values
    })

    fig_cat = px.bar(
        df_top_10_cat,
        x='Número de transações',
        y='Categoria',
        title="Top 10 categorias por número de transações",
        orientation='h',
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
        title=dict(text="Top 10 categorias por número de transações", font=dict(size=22), x=0.05),
        xaxis_title=dict(text="Número de transações", font=dict(size=18)),
        yaxis_title=dict(text="Categoria", font=dict(size=18)),
        yaxis={'categoryorder': 'total ascending'},
        legend=dict(font=dict(size=14)),
        legend_title=dict(font=dict(size=16))
    )

    fig_estab.update_traces(
        texttemplate='%{text:,}',
        textposition='inside'
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_estab, use_container_width=True, key="grafico_estabelecimentos")
    with col2:
        st.plotly_chart(fig_cat, use_container_width=True, key="grafico_categorias")

    # --- Top 10 bairros ---
    top_10_bairros = df['bairro_estabelecimento'].value_counts().head(10)
    df_top_10_bairros = pd.DataFrame({
        'Bairro': top_10_bairros.index,
        'Número de transações': top_10_bairros.values
    })
    fig_bairros = px.bar(
        df_top_10_bairros,
        x='Número de transações',
        y='Bairro',
        title="Top 10 bairros por número de transações",
        orientation='h',
        color='Número de transações',
        color_continuous_scale=[
            '#e5f5e0', '#a1d99b', '#74c476', '#31a354', '#006d2c'
        ],
        text='Número de transações'
    )
    fig_bairros.update_layout(
        title=dict(text="Top 10 bairros por número de transações", font=dict(size=22), x=0.05),
        xaxis_title=dict(text="Número de transações", font=dict(size=18)),
        yaxis_title=dict(text="Bairro", font=dict(size=18)),
        yaxis={'categoryorder': 'total ascending'},
        legend=dict(font=dict(size=14)),
        legend_title=dict(font=dict(size=16))
    )
    fig_bairros.update_traces(
        texttemplate='%{text:,}',
        textposition='inside'
    )

    # --- Top 10 produtos ---
    top_10_cupons = df['tipo_cupom'].value_counts().head(10)
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
        xaxis_title=dict(text="Número de transações", font=dict(size=18)),
        yaxis_title=dict(text="Tipo de cupom", font=dict(size=18)),
        yaxis={'categoryorder': 'total ascending'},
        legend=dict(font=dict(size=14)),
        legend_title=dict(font=dict(size=16))
    )
    fig_cupons.update_traces(
        texttemplate='%{text:,}',
        textposition='inside'
    )

    # --- Mostrar os dois novos gráficos lado a lado ---
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig_bairros, use_container_width=True, key="grafico_bairros")
    with col4:
        st.plotly_chart(fig_cupons, use_container_width=True, key="grafico_cupons")

except FileNotFoundError:
    st.error("Erro: O arquivo 'Base_de_Transacoes_Cupons_Capturados.csv' não foi encontrado.")
    st.info("Por favor, verifique se o arquivo está na pasta correta.")
except KeyError as e:
    st.error(f"Erro: A coluna {e} não foi encontrada. Verifique se o nome da coluna no seu arquivo .CSV está correto.")
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")

# Perfil dos clientes e Paulista

st.markdown("""
<div class="info-section">
    <div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-cart-shopping"></i> Perfil dos clientes</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

try:
    df = pd.read_csv("data/Base_Simulada_Pedestres_Av_Paulista.csv", sep=';', encoding='MacRoman')

    # Histograma: Idade

    nbins = 10
    df['faixa_idade'] = pd.cut(df['idade'], bins=nbins)

    grouped = df['faixa_idade'].value_counts().sort_index().reset_index()
    grouped.columns = ['faixa_idade', 'Quantidade']

    def fmt_interval(iv):
        l = int(np.floor(iv.left))
        r = int(np.ceil(iv.right))
        return f"{l}–{r}"

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
        xaxis_title=dict(text="Faixa de idade", font=dict(size=18)),
        yaxis_title=dict(text="Quantidade de usuários", font=dict(size=18)),
        bargap=0.05,
        showlegend=False
    )

    fig_idade.update_traces(
        marker_line_color="black",
        marker_line_width=0.5,
        texttemplate='%{text:,}',
        textposition='inside'
    )

    fig_idade.update_xaxes(tickangle=0, tickfont=dict(size=15))

    # Montante gasto por faixa de idade

    gasto_por_faixa = df.groupby('faixa_idade')['ultimo_valor_capturado'].sum().reset_index()
    gasto_por_faixa['faixa'] = gasto_por_faixa['faixa_idade'].apply(fmt_interval)
    gasto_por_faixa = gasto_por_faixa.sort_values('faixa_idade')

    fig_gasto = px.bar(
        gasto_por_faixa,
        x='faixa',
        y='ultimo_valor_capturado',
        text='ultimo_valor_capturado',
        title="Montante gasto por faixa de idade",
        color='ultimo_valor_capturado',
        color_continuous_scale=['#e5f5e0','#a1d99b','#74c476','#31a354','#006d2c']
    )

    fig_gasto.update_layout(
        title=dict(text="Montante gasto por faixa de idade", font=dict(size=22), x=0.05),
        xaxis_title=dict(text="Faixa de idade", font=dict(size=18)),
        yaxis_title=dict(text="Montante gasto", font=dict(size=18)),
        coloraxis_colorbar=dict(title="Montante gasto"),
        bargap=0.05,
    )

    fig_gasto.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='inside'
    )

    fig_gasto.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='inside'
    )

    fig_gasto.update_xaxes(tickangle=0, tickfont=dict(size=15))

    # Gráfico de rosca: Sexo

    sexo_counts = df['sexo'].value_counts().reset_index()
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
        textinfo="percent+label+value",
    )

    fig_sexo.update_layout(
    title=dict(text="Proporção de usuários por sexo", font=dict(size=22), x=0.05),
    legend_title=dict(font=dict(size=15)),
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    )
    )

    # Modelo de celular

    modelo_counts = df['modelo_celular'].value_counts().reset_index()
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
        xaxis_title=dict(text="Quantidade de usuários", font=dict(size=18)),
        yaxis_title=dict(text="Modelo de Celular", font=dict(size=18)),
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )

    fig_modelo.update_traces(
        texttemplate='%{text:,}',
        textposition='inside'
    )

    # Faixa de horários

    df['horario'] = pd.to_datetime(df['horario'], format='%H:%M:%S', errors='coerce').dt.time

    def faixa_horario(h):
        if h >= pd.to_datetime('00:00:00').time() and h <= pd.to_datetime('11:59:59').time():
            return 'Manhã'
        elif h >= pd.to_datetime('12:00:00').time() and h <= pd.to_datetime('18:59:59').time():
            return 'Tarde'
        else:
            return 'Noite'

    df['faixa_horario'] = df['horario'].apply(faixa_horario)

    horario_counts = df['faixa_horario'].value_counts().reindex(['Manhã','Tarde','Noite']).reset_index()
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
        xaxis_title=dict(text="Faixa de horário", font=dict(size=18)),
        yaxis_title=dict(text="Quantidade de registros", font=dict(size=18)),
        bargap=0.1,
        showlegend=False
    )

    fig_horario.update_traces(
        marker_line_color="black",
        marker_line_width=0.5,
        texttemplate='%{text:,}',
        textposition='inside'
    )

    # Principais locais

    top_locais = df['local'].value_counts().head(10).reset_index()
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
        xaxis_title=dict(text="Quantidade de registros", font=dict(size=18)),
        yaxis_title=dict(text="Local", font=dict(size=18)),
        yaxis={'categoryorder':'total ascending'},
        showlegend=False
    )

    fig_local.update_traces(
        texttemplate='%{text:,}',
        textposition='inside'
    )

    # Mostrar lado a lado

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_idade, use_container_width=True, key="grafico_idade")
    with col2:
        st.plotly_chart(fig_gasto, use_container_width=True, key="grafico_gasto")

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig_sexo, use_container_width=True, key="grafico_sexo")
    with col4:
        st.plotly_chart(fig_modelo, use_container_width=True, key="grafico_modelo")

    st.markdown("""
    <div class="info-section">
        <div class="bar"></div>
        <div class="info-content-wrapper">
            <div class="info-text-col">
                <div class="info-title"><i class="fa-solid fa-road"></i> Detalhamento: Avenida Paulista</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(fig_horario, use_container_width=True, key="grafico_horario")
    with col6:
        st.plotly_chart(fig_local, use_container_width=True, key="grafico_local")     

except FileNotFoundError:
    st.error("Erro: O arquivo 'Base_Simulada_Pedestres_Av_Paulista.csv' não foi encontrado.")
except KeyError as e:
    st.error(f"Erro: A coluna {e} não foi encontrada. Verifique o nome no CSV.")
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")

# Dados demográficos

st.markdown("""
<div class="info-section">
    <div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-map-location-dot"></i> Dados demográficos</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

try:
    df_players = pd.read_csv("data/Base_Cadastral_de_Players.csv", sep=';', encoding='MacRoman')

    # --- Cidade Residencial ---
    cidade_res_counts = df_players['cidade_residencial'].value_counts().reset_index().head(10)
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
        xaxis_title=dict(text="Quantidade de usuários", font=dict(size=18)),
        yaxis_title=dict(text="Cidade Residencial", font=dict(size=18)),
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )
    fig_cidade_res.update_traces(
        texttemplate='%{text:,}',
        textposition='outside'
    )

    # --- Bairro Residencial ---
    bairro_res_counts = df_players['bairro_residencial'].value_counts().reset_index().head(10)
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
        xaxis_title=dict(text="Quantidade de usuários", font=dict(size=18)),
        yaxis_title=dict(text="Bairro Residencial", font=dict(size=18)),
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )
    fig_bairro_res.update_traces(
        texttemplate='%{text:,}',
        textposition='inside'
    )

    # --- Cidade Trabalho ---
    cidade_trab_counts = df_players['cidade_trabalho'].value_counts().reset_index()
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
        xaxis_title=dict(text="Quantidade de usuários", font=dict(size=18)),
        yaxis_title=dict(text="Cidade de Trabalho", font=dict(size=18)),
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )
    fig_cidade_trab.update_traces(
        texttemplate='%{text:,}',
        textposition='inside'
    )

    # --- Bairro Trabalho ---
    bairro_trab_counts = df_players['bairro_trabalho'].value_counts().reset_index().head(10)
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
        xaxis_title=dict(text="Quantidade de usuários", font=dict(size=18)),
        yaxis_title=dict(text="Bairro de Trabalho", font=dict(size=18)),
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )
    fig_bairro_trab.update_traces(
        texttemplate='%{text:,}',
        textposition='inside'
    )

    # --- Mostrar gráficos ---
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_cidade_res, use_container_width=True, key="grafico_cidade_res")
    with col2:
        st.plotly_chart(fig_bairro_res, use_container_width=True, key="grafico_bairro_res")

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig_cidade_trab, use_container_width=True, key="grafico_cidade_trab")
    with col4:
        st.plotly_chart(fig_bairro_trab, use_container_width=True, key="grafico_bairro_trab")

except FileNotFoundError:
    st.error("Erro: O arquivo 'Base_Cadastral_de_Players.csv' não foi encontrado.")
except KeyError as e:
    st.error(f"Erro: A coluna {e} não foi encontrada. Verifique o nome no CSV.")
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")

# Footer

inject_footer()