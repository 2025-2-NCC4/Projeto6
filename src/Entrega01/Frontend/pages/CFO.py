import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from styles.footer import inject_footer
from styles.main import inject_global_styles
from styles.particles import inject_particles  
 
# Configurações da página

st.set_page_config(
    page_title="CFO",
    page_icon="💰",
    layout="wide"
)

inject_global_styles()

inject_particles()

# Utilitário de leitura com cache

@st.cache_data(show_spinner="Carregando dados do CSV")
def load_csv(path: str, sep: str = ';', encoding: str = 'MacRoman', **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, sep=sep, encoding=encoding, **kwargs)

# Helpers de formatação e conversão
def _to_numeric_br(series: pd.Series) -> pd.Series:
    """Converte strings no formato brasileiro (1.234.567,89) para float."""
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
    # En-US -> pt-BR
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

# Seção de informações

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            
<div class="info-section">
    <div class="info-content-wrapper">
        <div class="info-text-col">
            <div class="info-title"><i class="fa-solid fa-money-bill-trend-up"></i> Painel executivo: Chief Financial Officer - CFO</div>
            <div class="info-description">
                O painel do CFO oferece uma visão abrangente do desempenho financeiro da empresa, destacando métricas essenciais de receitas, despesas e lucros. Com gráficos interativos e análises detalhadas, o CFO pode monitorar a saúde financeira da organização, identificar tendências de mercado e tomar decisões estratégicas informadas para impulsionar o sucesso a longo prazo.
            </div>
        </div>
        <div class="info-image-col">
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

# Volumetrias

st.markdown("""
<div class="info-section">
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

df = load_csv("data/Base_de_Transacoes_Cupons_Capturados.csv", sep=';', encoding='MacRoman')

# Conversões de colunas numéricas

valor = _to_numeric_br(df.get("valor_cupom")) if "valor_cupom" in df.columns else pd.Series(dtype=float)
repasse = _to_numeric_br(df.get("repasse_picmoney")) if "repasse_picmoney" in df.columns else pd.Series(dtype=float)

# Cálculos principais

receita_total = float(np.nansum(valor)) if not valor.empty else 0.0
receita_moneybr = float(np.nansum(repasse)) if not repasse.empty else 0.0
cupons_capturados = int(len(df))
ticket_medio = (receita_total / cupons_capturados) if cupons_capturados > 0 else 0.0
receita_liquida = receita_total - receita_moneybr
margem_operacional = (receita_liquida / receita_total) if receita_total > 0 else 0.0
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
<div class="kpi-title">Receita total</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-money-check-dollar"></i></div>
</div>
<div class="kpi-value">{receita_total_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Receita Money BR</div>
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
<div class="kpi-title">Ticket médio</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-chart-line"></i></div>
</div>
<div class="kpi-value">{ticket_medio_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Margem Operacional</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-percent"></i></div>
</div>
<div class="kpi-value">{margem_operacional_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Usuários ativos</div>
<div class="kpi-icon-circle"><i class="fa-solid fa-user-group"></i></div>
</div>
<div class="kpi-value">{usuarios_ativos_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header">
<div class="kpi-title">Lojas ativas</div>
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
.kpi-title { color: #AAB3C0; font-size: 14px; font-weight: bold; font-family: Inter; }
.kpi-icon-circle { width: 36px; height: 36px; border-radius: 10px; background: #007031; display:flex; align-items:center; justify-content:center; }
.kpi-icon-circle i { color: #fff !important; font-size: 16px; }
.kpi-value { color: #fff; font-size: 28px; font-weight: 800; font-family: Inter; }
</style>
""",
    unsafe_allow_html=True,
)

# Lojas

st.markdown("""
<div class="info-section">
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

# Opções de lojas

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

# Recalcula métricas com filtro
valor_f = _to_numeric_br(df_filtered.get("valor_cupom")) if "valor_cupom" in df_filtered.columns else pd.Series(dtype=float)
repasse_f = _to_numeric_br(df_filtered.get("repasse_picmoney")) if "repasse_picmoney" in df_filtered.columns else pd.Series(dtype=float)

receita_total_f = float(np.nansum(valor_f)) if not valor_f.empty else 0.0
receita_moneybr_f = float(np.nansum(repasse_f)) if not repasse_f.empty else 0.0
cupons_capturados_f = int(len(df_filtered))
ticket_medio_f = (receita_total_f / cupons_capturados_f) if cupons_capturados_f > 0 else 0.0
receita_liquida_f = receita_total_f - receita_moneybr_f
margem_operacional_f = (receita_liquida_f / receita_total_f) if receita_total_f > 0 else 0.0
usuarios_ativos_f = int(df_filtered["celular"].nunique(dropna=True)) if "celular" in df_filtered.columns else 0

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
ticket_medio_f_fmt = _fmt_currency_br(ticket_medio_f)
margem_operacional_f_fmt = _fmt_pct(margem_operacional_f)
usuarios_ativos_f_fmt = _fmt_int_br(usuarios_ativos_f)
cupons_capturados_f_fmt = _fmt_int_br(cupons_capturados_f)

# Grid com KPIs filtrados
st.markdown(
    f"""
<div class="kpi-grid">
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Receita total</div><div class="kpi-icon-circle"><i class="fa-solid fa-money-check-dollar"></i></div></div>
<div class="kpi-value">{receita_total_f_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Receita Money BR</div><div class="kpi-icon-circle"><i class="fa-solid fa-wallet"></i></div></div>
<div class="kpi-value">{receita_moneybr_f_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Receita líquida</div><div class="kpi-icon-circle"><i class="fa-solid fa-signal"></i></div></div>
<div class="kpi-value">{receita_liquida_f_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Ticket médio</div><div class="kpi-icon-circle"><i class="fa-solid fa-chart-line"></i></div></div>
<div class="kpi-value">{ticket_medio_f_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Margem Operacional</div><div class="kpi-icon-circle"><i class="fa-solid fa-percent"></i></div></div>
<div class="kpi-value">{margem_operacional_f_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Usuários ativos</div><div class="kpi-icon-circle"><i class="fa-solid fa-user-group"></i></div></div>
<div class="kpi-value">{usuarios_ativos_f_fmt}</div>
</div>
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Nome da loja</div><div class="kpi-icon-circle"><i class="fa-solid fa-store"></i></div></div>
<div class="kpi-value">{nome_loja_text}</div>
</div>
<div class="kpi-card">
<div class="kpi-header"><div class="kpi-title">Cupons capturados</div><div class="kpi-icon-circle"><i class="fa-solid fa-ticket"></i></div></div>
<div class="kpi-value">{cupons_capturados_f_fmt}</div>
</div>
</div>
""",
    unsafe_allow_html=True,
)

# ===================== Gráfico: Receita Money BR por dia (Julho) ===================== #

if "data" in df_filtered.columns and "repasse_picmoney" in df_filtered.columns:
    data_dt = pd.to_datetime(df_filtered["data"], dayfirst=True, errors="coerce")
    repasse_num = _to_numeric_br(df_filtered["repasse_picmoney"]).fillna(0.0)

    plot_df = pd.DataFrame({"data": data_dt, "repasse": repasse_num})
    plot_df = plot_df.dropna(subset=["data"])  # remove datas inválidas
    # Foco no mês 7 (Julho)
    plot_df = plot_df[plot_df["data"].dt.month == 7]
    # Cria coluna explícita de dia para evitar uso do índice no groupby
    plot_df = plot_df.assign(dia=plot_df["data"].dt.date)

    daily = (
        plot_df
        .groupby("dia", as_index=False)["repasse"].sum()
        .rename(columns={"repasse": "receita_money_br"})
    )

    if not daily.empty:
        fig = px.line(
            daily,
            x="dia",
            y="receita_money_br",
            markers=True,
            title="Receita Money BR por dia (Julho)",
        )
        fig.update_traces(line_color="#007031")
        fig.update_layout(margin=dict(l=40, r=20, t=60, b=40), height=380)
        fig.update_yaxes(tickprefix="R$ ")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados de Julho para as lojas selecionadas.")
else:
    st.info("Colunas 'data' e/ou 'repasse_picmoney' não encontradas na base.")
