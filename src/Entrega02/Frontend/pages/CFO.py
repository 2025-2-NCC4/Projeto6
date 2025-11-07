import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from styles.footer import inject_footer
from styles.main import inject_global_styles
from styles.particles import inject_particles
from Backend.pdf_builder import build_cfo_pdf
import base64

# Configurações da página

st.set_page_config(
    page_title="CFO",
    page_icon="assets/cfo-icon.png",
    layout="wide"
)

inject_global_styles()

inject_particles()

# Utilitário de leitura com cache

def load_csv(path: str, sep: str = ';', encoding: str = 'MacRoman', **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, sep=sep, encoding=encoding, **kwargs)

# Helpers de formatação e conversão

def _to_numeric_br(series: pd.Series) -> pd.Series:
    if series.dtype == "O":
        s = (
            series.astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        return pd.to_numeric(s, errors="coerce")
    return pd.to_numeric(series, errors="coerce")

def _fmt_currency_br(value: float) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        value = 0.0
    txt = f"{value:,.2f}"
    txt = txt.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {txt}"

def _fmt_int_br(value: int) -> str:
    try:
        txt = f"{int(value):,}"
        return txt.replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0"

def _fmt_pct(value: float) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        value = 0.0
    return f"{value*100:.1f}%"

# Formatação compacta

def _fmt_currency_compact_br(value: float) -> str:
    try:
        v = float(value) if value is not None else 0.0
    except Exception:
        v = 0.0
    av = abs(v)
    if av >= 1_000_000_000:
        s = f"{v/1_000_000_000:.1f}".replace(".", ",")
        return f"{s} bi"
    if av >= 1_000_000:
        s = f"{v/1_000_000:.1f}".replace(".", ",")
        return f"{s} mi"
    if av >= 1_000:
        s = f"{v/1_000:.1f}".replace(".", ",")
        return f"{s} mil"
    return _fmt_currency_br(v)

def _fmt_int_compact_br(value: float) -> str:
    try:
        v = float(value) if value is not None else 0.0
    except Exception:
        v = 0.0
    av = abs(v)
    if av >= 1_000_000_000:
        s = f"{v/1_000_000_000:.1f}".replace(".", ",")
        return f"{s} bi"
    if av >= 1_000_000:
        s = f"{v/1_000_000:.1f}".replace(".", ",")
        return f"{s} mi"
    if av >= 1_000:
        s = f"{v/1_000:.1f}".replace(".", ",")
        return f"{s} mil"
    return _fmt_int_br(int(round(v)))

# Seção de informações

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            
<div class="info-section">
    <div class="info-content-wrapper">
        <div class="info-left-col">
            <div class="info-title-main"><i class="fa-solid fa-money-bill-trend-up"></i> Painel executivo: Chief Financial Officer - CFO</div>
            <div class="info-description">
                O painel do CFO oferece uma visão abrangente do desempenho financeiro da empresa, destacando métricas essenciais de receitas, despesas e lucros. Com gráficos interativos e análises detalhadas, o CFO pode monitorar a saúde financeira da organização, identificar tendências de mercado e tomar decisões estratégicas informadas para impulsionar o sucesso a longo prazo.
                <br>
                <br>
                <span class="explore-sections-title">Explore as seções!</span>
            </div>
            <div class="navigation-bar">
                <a href="#volumetrias-totais" class="nav-button">
                    <i class="fa-solid fa-chart-pie"></i> Volumetrias totais
                </a>
                <a href="#detalhamento-lojistas" class="nav-button">
                    <i class="fa-solid fa-shop"></i> Detalhamento dos lojistas
                </a>
                <a href="#detalhamento-cupons" class="nav-button">
                    <i class="fa-solid fa-receipt"></i> Detalhamento dos cupons
                </a>
                <a href="#correlacoes" class="nav-button">
                    <i class="fa-solid fa-arrow-trend-up"></i> Correlações
                </a>
            </div>
            <div class="info-description">
                <br>
                <span class="explore-sections-title">Visão executiva:</span>
            </div>
            <div class="navigation-bar">
                <a href="/CEO" class="nav-button">
                    <i class="fa-solid fa-briefcase"></i> Painel CEO
                </a>
            </div>
        </div>

<div class="info-right-col">
            <img src="https://raw.githubusercontent.com/2025-2-NCC4/Projeto6/refs/heads/main/imagens/charts-cfo.jpg" style="width: 100%; border-radius: 10px;">
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
            
.fa-solid {
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

# Volumetrias

st.markdown("""
<div id="volumetrias-totais" class="info-section">
    <div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-chart-pie"></i> Painel com volumetrias totais</div>
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

# Carrega a base

with st.spinner("Processando dados..."):
    df = load_csv("data/Base_de_Transacoes_Cupons_Capturados.csv")

# Conversões de colunas numéricas

valor = _to_numeric_br(df.get("valor_cupom")) if "valor_cupom" in df.columns else pd.Series(dtype=float)
repasse = _to_numeric_br(df.get("repasse_picmoney")) if "repasse_picmoney" in df.columns else pd.Series(dtype=float)

# Cálculos principais

receita_total = float(np.nansum(valor)) if not valor.empty else 0.0
receita_moneybr = float(np.nansum(repasse)) if not repasse.empty else 0.0
cupons_capturados = int(len(df))
ticket_medio = (receita_total / cupons_capturados) if cupons_capturados > 0 else 0.0
receita_liquida = receita_total - receita_moneybr
margem_operacional = (receita_moneybr / receita_total) if receita_total > 0 else 0.0
lojas_ativas = int(df["nome_estabelecimento"].nunique(dropna=True)) if "nome_estabelecimento" in df.columns else 0
usuarios_ativos = int(df["celular"].nunique(dropna=True)) if "celular" in df.columns else 0

# Formatações

receita_total_fmt = _fmt_currency_br(receita_total)
ticket_medio_fmt = _fmt_currency_br(ticket_medio)
receita_moneybr_fmt = _fmt_currency_br(receita_moneybr)
margem_operacional_fmt = _fmt_pct(margem_operacional)
lojas_ativas_fmt = _fmt_int_br(lojas_ativas)
cupons_capturados_fmt = _fmt_int_br(cupons_capturados)
usuarios_ativos_fmt = _fmt_int_br(usuarios_ativos)
receita_liquida_fmt = _fmt_currency_br(receita_liquida)

# Grid de cards de KPIs

st.markdown(
    f"""
<div class="kpi-grid">
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Repasse Money BR</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-wallet"></i></div>
</div>
<div class="kpi-value">{receita_moneybr_fmt}</div>

</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Receita líquida</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-signal"></i></div>
</div>
<div class="kpi-value">{receita_liquida_fmt}</div>

</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Receita total</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-money-check-dollar"></i></div>
</div>
<div class="kpi-value">{receita_total_fmt}</div>


</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Ticket médio</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-chart-line"></i></div>
</div>
<div class="kpi-value">{ticket_medio_fmt}</div>

</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Margem operacional</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-percent"></i></div>
</div>
<div class="kpi-value">{margem_operacional_fmt}</div>

</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Usuários</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-user-group"></i></div>
</div>
<div class="kpi-value">{usuarios_ativos_fmt}</div>

</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Lojas</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-store"></i></div>
</div>
<div class="kpi-value">{lojas_ativas_fmt}</div>

</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Cupons capturados</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-ticket"></i></div>
</div>
<div class="kpi-value">{cupons_capturados_fmt}</div>
</div>
</div>
""",
    unsafe_allow_html=True,
)

# Estilos

st.markdown(
    """
<style>
.kpi-grid {
    margin: 0 60px 30px 60px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
}
@media (max-width: 1200px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 700px) {
  .kpi-grid { grid-template-columns: 1fr; }
}
.kpi-card {
    background: #101414;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.18);
}
.kpi-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.kpi-title { color: #FFF; font-size: 16px; font-weight: bold; font-family: Inter; }
.kpi-icon-circle { width: 36px; height: 36px; border-radius: 10px; background: #007031; display:flex; align-items:center; justify-content:center; }
.kpi-icon-circle i { color: #fff !important; font-size: 16px; }
.kpi-value { color: #fff; font-size: 28px; font-weight: 800; font-family: Inter; }
</style>
""",
    unsafe_allow_html=True,
)

# Lojas

st.markdown("""
<div id="detalhamento-lojistas" class="info-section">
    <div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-shop"></i> Detalhamento dos lojistas</div>
        </div>
    </div>
</div>
<style>
.info-title {
    color: #007031;
    font-size: 30px;
    font-family: Inter;
    font-weight: bold;
    margin-bottom: 2px;
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
<div class="filter-toolbar">
    <div class="filter-title"><i class="fa-solid fa-sliders"></i> Filtrar lojistas</div>
</div>
""",
        unsafe_allow_html=True,
)

# Opções de lojas

store_options = []
if "nome_estabelecimento" in df.columns:
    store_options = sorted([s for s in df["nome_estabelecimento"].dropna().unique()])

selected_stores = st.multiselect(
    label="",
    options=store_options,
    default=store_options,
    placeholder="Selecione uma ou mais lojas",
    label_visibility="collapsed",
)

df_filtered = (
    df[df["nome_estabelecimento"].isin(selected_stores)]
    if selected_stores and len(selected_stores) > 0 and "nome_estabelecimento" in df.columns
    else df
)

# Valores com filtro

valor_f = _to_numeric_br(df_filtered.get("valor_cupom")) if "valor_cupom" in df_filtered.columns else pd.Series(dtype=float)
repasse_f = _to_numeric_br(df_filtered.get("repasse_picmoney")) if "repasse_picmoney" in df_filtered.columns else pd.Series(dtype=float)

receita_total_f = float(np.nansum(valor_f)) if not valor_f.empty else 0.0
receita_moneybr_f = float(np.nansum(repasse_f)) if not repasse_f.empty else 0.0
cupons_capturados_f = int(len(df_filtered))
receita_liquida_f = receita_total_f - receita_moneybr_f

if selected_stores is None or len(selected_stores) == 0 or len(selected_stores) == len(store_options):
    nome_loja_text = "Todas as lojas"
elif len(selected_stores) == 1:
    nome_loja_text = selected_stores[0]
else:
    nome_loja_text = f"{len(selected_stores)} lojas"

# Formatação

receita_total_f_fmt = _fmt_currency_br(receita_total_f)
receita_moneybr_f_fmt = _fmt_currency_br(receita_moneybr_f)
receita_liquida_f_fmt = _fmt_currency_br(receita_liquida_f)
cupons_capturados_f_fmt = _fmt_int_br(cupons_capturados_f)

# KPIs filtrados

st.markdown(
    f"""
<div class="kpi-grid">
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Nome da loja</div><div class="kpi-icon-circle"><i class="fa-solid fa-store"></i></div></div>
<div class="kpi-value">{nome_loja_text}</div>
</div>
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Repasse Money BR</div><div class="kpi-icon-circle"><i class="fa-solid fa-wallet"></i></div></div>
<div class="kpi-value">{receita_moneybr_f_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Receita líquida</div><div class="kpi-icon-circle"><i class="fa-solid fa-signal"></i></div></div>
<div class="kpi-value">{receita_liquida_f_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Receita total</div><div class="kpi-icon-circle"><i class="fa-solid fa-money-check-dollar"></i></div></div>
<div class="kpi-value">{receita_total_f_fmt}</div>
</div>
</div>
""",
    unsafe_allow_html=True,
)

# Gráficos

if "data" in df_filtered.columns and "repasse_picmoney" in df_filtered.columns:
    data_dt = pd.to_datetime(df_filtered["data"], dayfirst=True, errors="coerce")
    repasse_num = _to_numeric_br(df_filtered["repasse_picmoney"]).fillna(0.0)

    plot_df = pd.DataFrame({"data": data_dt, "repasse": repasse_num})
    plot_df = plot_df.dropna(subset=["data"]) 
    plot_df = plot_df[pd.to_datetime(plot_df["data"]).dt.month == 7]
    plot_df = plot_df.assign(dia=pd.to_datetime(plot_df["data"]).dt.normalize())

    daily = (
        plot_df
        .groupby("dia", as_index=False)["repasse"].sum()
        .rename(columns={"repasse": "receita_money_br"})
    )

    if not daily.empty:
        _left_gutter, c1, c2, _right_gutter = st.columns([0.03, 0.47, 0.47, 0.03])
        ano = int(pd.to_datetime(daily["dia"]).dt.year.mode().iloc[0])
        dias_no_mes = pd.Period(f"{ano}-07").days_in_month
        todos_os_dias = pd.date_range(f"{ano}-07-01", periods=dias_no_mes, freq="D")
        daily_full = (
            daily.set_index("dia")
                 .reindex(todos_os_dias, fill_value=0.0)
                 .rename_axis("dia")
                 .reset_index()
        )

        fig = px.line(
            daily_full,
            x="dia",
            y="receita_money_br",
            markers=True,
            title="Receita Money BR por dia",
        )
        fig.update_traces(line_color="#007031")
        fig.update_xaxes(dtick="D1", tickformat="%d")
        fig.update_yaxes(tickprefix="R$ ")
        fig.update_layout(
            title=dict(text="Repasse (R$) Money BR em julho de 2025", font=dict(size=22), x=0.05),
            xaxis_title=dict(text="Dias", font=dict(size=22)),
            yaxis_title=dict(text="Valor", font=dict(size=22)),
            xaxis=dict(tickfont=dict(size=16)),
            yaxis=dict(tickfont=dict(size=16))
        )
        c1.plotly_chart(fig, use_container_width=True)

        # Cupons capturados por dia
        count_df = pd.DataFrame({"data": data_dt})
        count_df = count_df.dropna(subset=["data"])
        count_df = count_df[pd.to_datetime(count_df["data"]).dt.month == 7]
        count_df = count_df.assign(dia=pd.to_datetime(count_df["data"]).dt.normalize())
        daily_counts = (
            count_df
            .groupby("dia", as_index=False)
            .size()
            .rename(columns={"size": "cupons_capturados"})
        )
        if not daily_counts.empty:
            daily_counts_full = (
                daily_counts.set_index("dia")
                             .reindex(todos_os_dias, fill_value=0)
                             .rename_axis("dia")
                             .reset_index()
            )
            fig2 = px.line(
                daily_counts_full,
                x="dia",
                y="cupons_capturados",
                markers=True,
                title="Cupons capturados em julho de 2025",
            )
            fig2.update_traces(line_color="#007031")
            fig2.update_xaxes(dtick="D1", tickformat="%d")
            fig2.update_layout(title=dict(text="Cupons capturados em julho de 2025", font=dict(size=22), x=0.05),
                            xaxis_title=dict(text="Dias", font=dict(size=22)),
                            yaxis_title=dict(text="Quantidade", font=dict(size=22)),
                            xaxis=dict(tickfont=dict(size=16)),
                            yaxis=dict(tickfont=dict(size=16))
            )
            c2.plotly_chart(fig2, use_container_width=True)
        else:
            c2.info("Sem contagem de cupons para Julho nas lojas selecionadas.")
    else:
        st.info("Sem dados de Julho para as lojas selecionadas.")
else:
    st.info("Colunas 'data' e/ou 'repasse_picmoney' não encontradas na base.")

# Cupons

st.markdown("""
<div id="detalhamento-cupons" class="info-section">
    <div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-receipt"></i> Detalhamento dos cupons</div>
        </div>
    </div>
</div>
<style>
.info-title {
    color: #007031;
    font-size: 30px;
    font-family: Inter;
    font-weight: bold;
    margin-bottom: 2px;
}
</style>
""", unsafe_allow_html=True)

# Filtro por cupons (tipo_cupom)

tipo_options = []
if "tipo_cupom" in df_filtered.columns:
    tipo_options = sorted([t for t in df_filtered["tipo_cupom"].dropna().astype(str).unique()])

st.markdown(
    """
<div class="filter-toolbar">
    <div class="filter-title"><i class="fa-solid fa-sliders"></i> Filtrar cupons</div>
    
</div>
""",
    unsafe_allow_html=True,
)

selected_tipos = st.multiselect(
    label="",
    options=tipo_options,
    default=tipo_options,
    placeholder="Selecione um ou mais tipos de cupom",
    label_visibility="collapsed",
)

df_cupons = (
    df_filtered[df_filtered["tipo_cupom"].astype(str).isin(selected_tipos)]
    if selected_tipos and len(selected_tipos) > 0 and "tipo_cupom" in df_filtered.columns
    else df_filtered
)

# KPIs de cupons filtrados

valor_c = _to_numeric_br(df_cupons.get("valor_cupom")) if "valor_cupom" in df_cupons.columns else pd.Series(dtype=float)
repasse_c = _to_numeric_br(df_cupons.get("repasse_picmoney")) if "repasse_picmoney" in df_cupons.columns else pd.Series(dtype=float)

qtd_cupons_c = int(len(df_cupons))
receita_total_c = float(np.nansum(valor_c)) if not valor_c.empty else 0.0
receita_moneybr_c = float(np.nansum(repasse_c)) if not repasse_c.empty else 0.0
receita_liquida_c = receita_total_c - receita_moneybr_c

qtd_cupons_c_fmt = _fmt_int_br(qtd_cupons_c)
receita_total_c_fmt = _fmt_currency_br(receita_total_c)
receita_moneybr_c_fmt = _fmt_currency_br(receita_moneybr_c)
receita_liquida_c_fmt = _fmt_currency_br(receita_liquida_c)

st.markdown(
    f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-header"><div class="kpi-title">Quantidade de cupons</div><div class="kpi-icon-circle"><i class="fa-solid fa-ticket"></i></div></div>
    <div class="kpi-value">{qtd_cupons_c_fmt}</div>
  </div>
    <div class="kpi-card">
    <div class="kpi-header"><div class="kpi-title">Repasse Money BR</div><div class="kpi-icon-circle"><i class="fa-solid fa-wallet"></i></div></div>
    <div class="kpi-value">{receita_moneybr_c_fmt}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-header"><div class="kpi-title">Receita líquida</div><div class="kpi-icon-circle"><i class="fa-solid fa-signal"></i></div></div>
    <div class="kpi-value">{receita_liquida_c_fmt}</div>
  </div>
    <div class="kpi-card">
    <div class="kpi-header"><div class="kpi-title">Receita total</div><div class="kpi-icon-circle"><i class="fa-solid fa-money-check-dollar"></i></div></div>
    <div class="kpi-value">{receita_total_c_fmt}</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# Gráficos

_lg, col_lojas, col_bairros, _rg = st.columns([0.03, 0.47, 0.47, 0.03])

# Paleta de verdes

GREEN_SEQ = [ "#5EB161", "#6ee190", "#119131"]
color_map = {}
if "tipo_cupom" in df_cupons.columns:
    tipos_ordenados = sorted(df_cupons["tipo_cupom"].dropna().astype(str).unique())
    color_map = {t: GREEN_SEQ[i % len(GREEN_SEQ)] for i, t in enumerate(tipos_ordenados)}

# Top 10 lojas por valor

with col_lojas:
    if "nome_estabelecimento" in df_cupons.columns and "tipo_cupom" in df_cupons.columns:
        base_lojas = df_cupons.copy()
        base_lojas["valor_num"] = _to_numeric_br(base_lojas.get("valor_cupom")) if "valor_cupom" in base_lojas.columns else np.nan
        if base_lojas["valor_num"].notna().any():
            total_por_loja = base_lojas.groupby("nome_estabelecimento", as_index=False)["valor_num"].sum()
            top_lojas = total_por_loja.nlargest(10, "valor_num")["nome_estabelecimento"].tolist()
            agg = (
                base_lojas[base_lojas["nome_estabelecimento"].isin(top_lojas)]
                .groupby(["nome_estabelecimento", "tipo_cupom"], as_index=False)["valor_num"].sum()
                .rename(columns={"valor_num": "valor"})
            )
            y_label = "Valor"
        else:
            total_por_loja = base_lojas.groupby("nome_estabelecimento", as_index=False).size()
            top_lojas = total_por_loja.nlargest(10, "size")["nome_estabelecimento"].tolist()
            agg = (
                base_lojas[base_lojas["nome_estabelecimento"].isin(top_lojas)]
                .groupby(["nome_estabelecimento", "tipo_cupom"], as_index=False)
                .size()
                .rename(columns={"size": "valor"})
            )
            y_label = "Quantidade"

        if not agg.empty:
            if y_label == "Valor":
                agg["text_label"] = agg["valor"].apply(_fmt_currency_compact_br)
            else:
                agg["text_label"] = agg["valor"].apply(_fmt_int_compact_br)
            fig_l = px.bar(
                agg,
                x="nome_estabelecimento",
                y="valor",
                color="tipo_cupom",
                barmode="stack",
                title=f"Top 10 lojas por {y_label.lower()} (R$) de cupons (empilhado por tipo)",
                color_discrete_map=color_map,
                text="text_label",
            )
            fig_l.update_layout(
                xaxis_title=dict(text="Lojas", font=dict(size=22)),
                yaxis_title=dict(text=y_label, font=dict(size=22)),
                legend_title_text="Tipo de cupom",
                legend_title_font=dict(size=18),
                legend=dict(font=dict(size=15)),
                title=dict(x=0.05, font=dict(size=20)),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(tickfont=dict(size=16))
            )
            fig_l.update_xaxes(tickangle=-30)
            fig_l.update_traces(texttemplate="%{text}", textposition="inside", textfont_color="white", textfont_size=16)
            st.plotly_chart(fig_l, use_container_width=True)
        else:
            st.info("Sem dados suficientes para compor o gráfico de lojas.")
    else:
        st.info("Colunas necessárias não encontradas: 'nome_estabelecimento' e/ou 'tipo_cupom'.")

# Top 10 bairros por valor

with col_bairros:
    possiveis_bairros = [
        "bairro",
        "bairro_cliente",
        "bairro_estabelecimento",
        "bairro_loja",
    ]
    bairro_col = next((c for c in possiveis_bairros if c in df_cupons.columns), None)

    if bairro_col and "tipo_cupom" in df_cupons.columns:
        base_bairros = df_cupons.copy()
        base_bairros = base_bairros.dropna(subset=[bairro_col])
        base_bairros["valor_num"] = _to_numeric_br(base_bairros.get("valor_cupom")) if "valor_cupom" in base_bairros.columns else np.nan

        if base_bairros["valor_num"].notna().any():
            total_por_bairro = base_bairros.groupby(bairro_col, as_index=False)["valor_num"].sum()
            top_bairros = total_por_bairro.nlargest(10, "valor_num")[bairro_col].tolist()
            agg_b = (
                base_bairros[base_bairros[bairro_col].isin(top_bairros)]
                .groupby([bairro_col, "tipo_cupom"], as_index=False)["valor_num"].sum()
                .rename(columns={"valor_num": "valor"})
            )
            y_label_b = "Valor"
        else:
            total_por_bairro = base_bairros.groupby(bairro_col, as_index=False).size()
            top_bairros = total_por_bairro.nlargest(10, "size")[bairro_col].tolist()
            agg_b = (
                base_bairros[base_bairros[bairro_col].isin(top_bairros)]
                .groupby([bairro_col, "tipo_cupom"], as_index=False)
                .size()
                .rename(columns={"size": "valor"})
            )
            y_label_b = "Quantidade"

        if not agg_b.empty:
            # Labels compactas
            if y_label_b == "Valor":
                agg_b["text_label"] = agg_b["valor"].apply(_fmt_currency_compact_br)
            else:
                agg_b["text_label"] = agg_b["valor"].apply(_fmt_int_compact_br)
            fig_b = px.bar(
                agg_b,
                x=bairro_col,
                y="valor",
                color="tipo_cupom",
                barmode="stack",
                title=f"Top 10 bairros por {y_label_b.lower()} (R$) de cupons (empilhado por tipo)",
                color_discrete_map=color_map,
                text="text_label",
            )
            fig_b.update_layout(
                xaxis_title=dict(text="Bairros", font=dict(size=22)),
                yaxis_title=dict(text=y_label_b, font=dict(size=22)),
                legend_title_text="Tipo de cupom",
                legend_title_font=dict(size=18),
                legend=dict(font=dict(size=15)),
                title=dict(x=0.05, font=dict(size=20)),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(tickfont=dict(size=16)),
            )
            fig_b.update_xaxes(tickangle=-30)
            fig_b.update_traces(texttemplate="%{text}", textposition="inside", textfont_color="white", textfont_size=16)
            st.plotly_chart(fig_b, use_container_width=True)
        else:
            st.info("Sem dados suficientes para compor o gráfico de bairros.")
    else:
        st.info("Nenhuma coluna de bairro encontrada para montar o gráfico.")

st.markdown("""
<div class="info-section">
    <div class="bar"></div>
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div id="correlacoes" class="info-title">
                <i class="fa-solid fa-arrow-trend-up"></i> Correlações 
                <span 
                    class="custom-tooltip-wrapper" 
                    data-tooltip="Correlações medem o grau de relacionamento entre duas ou mais variáveis. Nesse painel, mostram como as tendências de diferentes métricas se movem juntas, ajudando a identificar padrões."
                >
                    <i class="fa-solid fa-circle-info"></i>
                </span>
            </div>
        </div>
    </div>
</div>
<style>
.info-title {
    font-size: 30px;
    font-family: Inter;
    font-weight: bold;
    margin-bottom: 2px;
    cursor: help;
}
.custom-tooltip-wrapper::before {
    content: attr(data-tooltip);
    visibility: hidden;
    opacity: 0;
    background-color: #333;
    color: #fff;
    font-family: Inter, sans-serif;
    font-size: 18px;
    text-align: left;
    padding: 8px 12px;
    border-radius: 6px;
    width: 300px; 
    white-space: normal;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    position: absolute;
    z-index: 1000;
    left: 20%;
    transform: translateX(-50%);
    transition: opacity 0.3s ease;
}
.custom-tooltip-wrapper::after {
    content: "";
    visibility: hidden;
    opacity: 0;
    border-width: 5px;
    border-style: solid;
    border-color: #333 transparent transparent transparent;
    position: absolute;
    z-index: 1000;
    bottom: 115%;
    left: 20%;
    transform: translateX(-50%);
    transition: opacity 0.3s ease;
}
.custom-tooltip-wrapper:hover::before,
.custom-tooltip-wrapper:hover::after {
    visibility: visible;
    opacity: 1;
}
.custom-tooltip-wrapper i { 
    color: inherit; 
}
        
</style>
""", unsafe_allow_html=True)

# Gráfico de correlação

_lg_corr, corr_left, corr_right, _rg_corr = st.columns([0.03, 0.47, 0.47, 0.03])

# Correlação: valor_cupom vs repasse_picmoney

with corr_left:
    if {"valor_cupom", "repasse_picmoney"}.issubset(df_cupons.columns):
        x_val = _to_numeric_br(df_cupons["valor_cupom"]).astype(float)
        y_rep = _to_numeric_br(df_cupons["repasse_picmoney"]).astype(float)
        mask = x_val.notna() & y_rep.notna()
        x = x_val[mask]
        y = y_rep[mask]

        if len(x) >= 2:

            # Pearson r

            r = float(np.corrcoef(x, y)[0, 1])
            abs_r = abs(r)
            if abs_r < 0.3:
                grau = "fraca"
            elif abs_r < 0.6:
                grau = "moderada"
            elif abs_r < 0.8:
                grau = "forte"
            else:
                grau = "muito forte"

            corr_df = pd.DataFrame({"Valor do cupom": x, "Repasse Money BR": y})
            fig_corr = px.scatter(
                corr_df,
                x="Valor do cupom",
                y="Repasse Money BR",
                title=f"Correlação linear Valor x Repasse (r = {r:.2f}, grau: {grau})",
            )

            # Trendline

            try:
                coeffs = np.polyfit(x, y, 1)
                x_min, x_max = float(x.min()), float(x.max())
                xs = np.array([x_min, x_max])
                ys = coeffs[0] * xs + coeffs[1]

                # Linha acima dos pontos

                fig_corr.add_shape(
                    type="line",
                    x0=x_min, y0=float(ys[0]), x1=x_max, y1=float(ys[1]),
                    xref="x", yref="y",
                    line=dict(color="#FFFFFF", width=4, dash="dash"),
                    layer="above",
                )
                fig_corr.update_traces(showlegend=False)
                fig_corr.add_trace(
                    go.Scatter(
                        x=xs,
                        y=ys,
                        mode="lines",
                        name=f"Tendência (r={r:.2f})",
                        line=dict(color="#023004", width=4, dash="dash"),
                        showlegend=True,
                        hoverinfo="skip",
                        visible="legendonly",
                    )
                )
            except Exception:
                pass

            fig_corr.update_traces(marker=dict(color="#196D0C"))
            fig_corr.update_layout(
                xaxis_title=dict(text="Valor do cupom", font=dict(size=22)),
                yaxis_title=dict(text="Repasse Money BR", font=dict(size=22)),
                title=dict(x=0.05, font=dict(size=20), pad=dict(b=14)),
                legend=dict(
                    orientation="h",
                    font=dict(size=14, color="#ffffff"),
                    x=0.05,
                    y=1.02,
                    xanchor="left",
                    yanchor="bottom",
                ),
                margin=dict(t=110),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(tickfont=dict(size=16)),
            )
            fig_corr.update_xaxes(tickprefix="R$ ")
            fig_corr.update_yaxes(tickprefix="R$ ")
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Dados insuficientes para calcular correlação.")
    else:
        st.info("Colunas 'valor_cupom' e/ou 'repasse_picmoney' não encontradas.")

# Linhas de tendência por tipo_cupom

with corr_right:
    required_cols = {"valor_cupom", "repasse_picmoney", "tipo_cupom"}
    if required_cols.issubset(df_cupons.columns):
        df_aux = df_cupons.copy()
        df_aux["x"] = _to_numeric_br(df_aux["valor_cupom"]).astype(float)
        df_aux["y"] = _to_numeric_br(df_aux["repasse_picmoney"]).astype(float)
        df_aux["tipo"] = df_aux["tipo_cupom"].astype(str)
        df_aux = df_aux[df_aux["x"].notna() & df_aux["y"].notna() & df_aux["tipo"].notna()]

        tipos = sorted(df_aux["tipo"].unique())
        color_map_local = {t: GREEN_SEQ[i % len(GREEN_SEQ)] for i, t in enumerate(tipos)}

        fig_lines = go.Figure()
        added = 0
        for t in tipos:
            sub = df_aux[df_aux["tipo"] == t]
            if len(sub) < 2:
                continue
            try:
                r = float(np.corrcoef(sub["x"], sub["y"])[0, 1])
                a, b = np.polyfit(sub["x"], sub["y"], 1)
                x_min_t = float(sub["x"].min())
                x_max_t = float(sub["x"].max())
                xs = np.array([x_min_t, x_max_t])
                ys = a * xs + b
                fig_lines.add_trace(
                    go.Scatter(
                        x=xs,
                        y=ys,
                        mode="lines",
                        name=f"{t} (r={r:.2f})",
                        line=dict(color=color_map_local.get(t, "#56ac37"), dash="dash", width=4),
                        showlegend=True,
                    )
                )
                added += 1
            except Exception:
                continue

        if added > 0:
            fig_lines.update_layout(
                title=dict(text="Tendências por tipo de cupom", x=0.05, font=dict(size=20), pad=dict(b=14)),
                xaxis_title=dict(text="Valor do cupom", font=dict(size=22)),
                yaxis_title=dict(text="Repasse Money BR", font=dict(size=22)),
                legend=dict(
                    orientation="h",
                    font=dict(size=14),
                    x=0.05,
                    y=1.02,
                    xanchor="left",
                    yanchor="bottom",
                ),
                margin=dict(t=110),
                xaxis=dict(tickfont=dict(size=16)),
                yaxis=dict(tickfont=dict(size=16)),
            )
            fig_lines.update_xaxes(tickprefix="R$ ")
            fig_lines.update_yaxes(tickprefix="R$ ")
            st.plotly_chart(fig_lines, use_container_width=True)
        else:
            st.info("Dados insuficientes por tipo para traçar linhas de tendência.")
    else:
        st.info("Colunas 'valor_cupom', 'repasse_picmoney' e/ou 'tipo_cupom' não encontradas.")

# Botão de gerar PDF estilizado e centralizado
st.markdown("""
<style>
.pdf-button-container {
    display: flex;
    justify-content: center;
    margin: 40px 0;
}
</style>
""", unsafe_allow_html=True)

# Container centralizado para o botão
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📄 Gerar Relatório em PDF", use_container_width=True, type="primary"):
        st.write("Gerando PDF com insights financeiros...")
        
        # Organiza os filtros
        filtros = {
            'lojas': selected_stores if selected_stores else store_options,
            'tipos_cupom': selected_tipos if selected_tipos else tipo_options
        }
        
        # Organiza os KPIs
        kpis = {
            'receita_total': receita_total,
            'receita_moneybr': receita_moneybr,
            'receita_liquida': receita_liquida,
            'cupons_capturados': cupons_capturados,
            'ticket_medio': ticket_medio,
            'margem_operacional': margem_operacional,
            'lojas_ativas': lojas_ativas,
            'usuarios_ativos': usuarios_ativos
        }
        
        # Organiza os dataframes necessários
        dataframes = {}
        
        # Prepara dataframe de cupons por tipo para análise
        if 'tipo_cupom' in df_cupons.columns:
            cupons_tipo = df_cupons.copy()
            if 'valor_cupom' in cupons_tipo.columns:
                cupons_tipo['valor_num'] = _to_numeric_br(cupons_tipo['valor_cupom'])
            else:
                cupons_tipo['valor_num'] = 0
            cupons_tipo_agg = (
                cupons_tipo.groupby('tipo_cupom', as_index=False)
                .agg({'valor_num': 'sum'})
                .rename(columns={'valor_num': 'valor', 'tipo_cupom': 'Tipo'})
                .sort_values('valor', ascending=False)
            )
            if not cupons_tipo_agg.empty:
                dataframes['df_cupons_tipo'] = cupons_tipo_agg
        
        # Diretório temporário para gráficos
        temp_dir = "/Users/pedrolemos/.gemini/tmp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        chart_paths = {}
        
        # Salva os gráficos que foram criados
        if 'fig' in locals() and fig:
            chart_paths['fig_repasse_dia'] = os.path.join(temp_dir, "fig_repasse_dia.png")
            fig.write_image(chart_paths['fig_repasse_dia'])
        
        if 'fig2' in locals() and fig2:
            chart_paths['fig_cupons_dia'] = os.path.join(temp_dir, "fig_cupons_dia.png")
            fig2.write_image(chart_paths['fig_cupons_dia'])
        
        if 'fig_l' in locals() and fig_l:
            # Salva tanto para receita quanto para cupons (mesmo gráfico usado em diferentes contextos)
            chart_paths['fig_lojas_receita'] = os.path.join(temp_dir, "fig_lojas_receita.png")
            chart_paths['fig_top_lojas'] = os.path.join(temp_dir, "fig_top_lojas.png")
            fig_l.write_image(chart_paths['fig_lojas_receita'])
            fig_l.write_image(chart_paths['fig_top_lojas'])
            # Prepara dataframe para análise
            if 'agg' in locals():
                dataframes['df_top_lojas_receita'] = agg
        
        if 'fig_b' in locals() and fig_b:
            # Salva tanto para bairro quanto para cupons (mesmo gráfico usado em diferentes contextos)
            chart_paths['fig_lojas_bairro'] = os.path.join(temp_dir, "fig_lojas_bairro.png")
            chart_paths['fig_top_bairros'] = os.path.join(temp_dir, "fig_top_bairros.png")
            fig_b.write_image(chart_paths['fig_lojas_bairro'])
            fig_b.write_image(chart_paths['fig_top_bairros'])
            if 'agg_b' in locals():
                dataframes['df_lojas_bairro'] = agg_b
        
        if 'fig_corr' in locals() and fig_corr:
            chart_paths['fig_correlacao'] = os.path.join(temp_dir, "fig_correlacao.png")
            fig_corr.write_image(chart_paths['fig_correlacao'])
            # Dados de correlação se disponíveis
            if 'r' in locals():
                dataframes['correlacao_valor'] = r
            if 'corr_df' in locals():
                dataframes['n_pontos'] = len(corr_df)
        
        if 'fig_lines' in locals() and fig_lines:
            chart_paths['fig_tendencias'] = os.path.join(temp_dir, "fig_tendencias.png")
            fig_lines.write_image(chart_paths['fig_tendencias'])
        
        # Gera o PDF com insights
        try:
            pdf_output = build_cfo_pdf(filtros, dataframes, chart_paths, temp_dir, kpis)
            b64 = base64.b64encode(pdf_output).decode('utf-8')
            
            # Link de download estilizado
            st.markdown(f"""
            <style>
            .download-container {{{{
                display: flex;
                justify-content: center;
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
                <a href="data:application/octet-stream;base64,{b64}" download="relatorio_cfo_completo.pdf" class="download-link">
                    📥 Download do Relatório CFO
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ PDF gerado com sucesso! Clique no botão acima para baixar.")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")
            import traceback
            st.code(traceback.format_exc())

# Footer

inject_footer()
