"""
Módulo com análises e insights estratégicos para o relatório CFO
"""

def get_executive_summary_cfo(kpis, filtros):
    """Retorna o sumário executivo com KPIs principais"""
    filtros_text = []
    if filtros.get('lojas'):
        filtros_text.append(f"Lojas: {', '.join(filtros['lojas'])}")
    else:
        filtros_text.append("Lojas: Todas")
        
    if filtros.get('tipos_cupom'):
        filtros_text.append(f"Tipos de Cupom: {', '.join(filtros['tipos_cupom'])}")
    else:
        filtros_text.append("Tipos de Cupom: Todos")
    
    return {
        'titulo': 'Sumário Executivo Financeiro',
        'descricao': (
            'Este relatório apresenta uma análise financeira estratégica da MoneyBR, '
            'com foco em receitas, margens operacionais, performance de parceiros e correlações. '
            'Os dados foram processados com os seguintes filtros aplicados.'
        ),
        'filtros': filtros_text,
        'kpis': kpis
    }

def analyze_volumetria_financeira(kpis):
    """Análise das volumetrias financeiras totais"""
    receita_total = kpis.get('receita_total', 0)
    receita_moneybr = kpis.get('receita_moneybr', 0)
    margem = kpis.get('margem_operacional', 0)
    ticket_medio = kpis.get('ticket_medio', 0)
    
    analysis = (
        f"A receita total de R$ {receita_total:,.2f} resulta em um repasse de "
        f"R$ {receita_moneybr:,.2f} para a MoneyBR, representando uma margem operacional "
        f"de {margem*100:.1f}%. O ticket médio de R$ {ticket_medio:.2f} indica o valor "
        "médio por transação, métrica fundamental para projeções de crescimento."
    )
    
    insights = [
        "Monitorar margem operacional para garantir sustentabilidade do modelo de negócio",
        "Aumentar ticket médio através de estratégias de upsell e cross-sell",
        "Otimizar estrutura de repasse para maximizar receita sem comprometer parceiros",
        "Estabelecer metas trimestrais de crescimento baseadas no histórico de performance"
    ]
    
    return analysis, insights

def analyze_receita_operacional(receita_total, receita_moneybr, receita_liquida):
    """Análise detalhada da estrutura de receitas"""
    percent_repasse = (receita_moneybr / receita_total * 100) if receita_total > 0 else 0
    percent_liquido = (receita_liquida / receita_total * 100) if receita_total > 0 else 0
    
    analysis = (
        f"Do total de R$ {receita_total:,.2f} transacionado, {percent_repasse:.1f}% "
        f"(R$ {receita_moneybr:,.2f}) constitui o repasse MoneyBR, enquanto "
        f"{percent_liquido:.1f}% (R$ {receita_liquida:,.2f}) representa a receita "
        "líquida dos estabelecimentos parceiros. Esta estrutura garante atratividade "
        "para ambas as partes no ecossistema."
    )
    
    insights = [
        "Avaliar impacto de ajustes na estrutura de repasse sobre volume de transações",
        "Criar tiers de parceria com margens diferenciadas baseadas em volume",
        "Negociar margens maiores com estabelecimentos de alto volume (poder de barganha)",
        "Implementar modelo dinâmico de precificação baseado em performance"
    ]
    
    return analysis, insights

def analyze_eficiencia_operacional(cupons_capturados, usuarios_ativos, lojas_ativas, 
                                   receita_total, receita_moneybr):
    """Análise de eficiência operacional"""
    receita_por_usuario = receita_total / usuarios_ativos if usuarios_ativos > 0 else 0
    receita_por_loja = receita_total / lojas_ativas if lojas_ativas > 0 else 0
    cupons_por_usuario = cupons_capturados / usuarios_ativos if usuarios_ativos > 0 else 0
    
    analysis = (
        f"Com {cupons_capturados:,} cupons capturados por {usuarios_ativos:,} usuários "
        f"em {lojas_ativas:,} lojas, temos uma média de {cupons_por_usuario:.1f} cupons "
        f"por usuário. A receita média por usuário é de R$ {receita_por_usuario:,.2f} "
        f"e por loja de R$ {receita_por_loja:,.2f}, indicadores cruciais de eficiência."
    )
    
    insights = [
        f"Aumentar frequência de uso: meta de elevar {cupons_por_usuario:.1f} para "
        f"{cupons_por_usuario * 1.5:.1f} cupons/usuário",
        "Identificar e replicar estratégias de lojas com maior receita média",
        "Desenvolver programa de gamificação para aumentar engajamento",
        "Criar alertas para usuários com queda de frequência (churn prevention)"
    ]
    
    return analysis, insights

def analyze_top_lojas_receita(df_top_lojas):
    """Análise das lojas por receita"""
    if df_top_lojas is None or len(df_top_lojas) == 0:
        return "Dados insuficientes para análise.", []
    
    # Debug: mostra as colunas disponíveis
    print(f"DEBUG analyze_top_lojas_receita - Colunas: {df_top_lojas.columns.tolist()}")
    
    # Detecta as colunas dinamicamente
    col_loja = 'nome_estabelecimento' if 'nome_estabelecimento' in df_top_lojas.columns else 'Loja'
    col_valor = 'valor' if 'valor' in df_top_lojas.columns else 'Receita Total'
    
    print(f"DEBUG - Usando colunas: loja={col_loja}, valor={col_valor}")
    
    # Agrupa por loja se houver múltiplas linhas por loja (tipos de cupom)
    if 'tipo_cupom' in df_top_lojas.columns:
        df_agregado = df_top_lojas.groupby(col_loja)[col_valor].sum().reset_index()
        df_agregado = df_agregado.sort_values(col_valor, ascending=False).head(10)
    else:
        df_agregado = df_top_lojas.copy()
    
    total_receita = df_agregado[col_valor].sum()
    loja_lider = df_agregado.iloc[0][col_loja]
    receita_lider = df_agregado.iloc[0][col_valor]
    percent_lider = (receita_lider / total_receita * 100) if total_receita > 0 else 0
    top_3_receita = df_agregado.head(3)[col_valor].sum()
    percent_top_3 = (top_3_receita / total_receita * 100) if total_receita > 0 else 0
    
    analysis = (
        f"A loja '{loja_lider}' lidera com R$ {receita_lider:,.2f} ({percent_lider:.1f}% "
        f"do total). As top 3 lojas concentram {percent_top_3:.1f}% da receita, "
        "evidenciando forte concentração e dependência de poucos parceiros estratégicos."
    )
    
    insights = [
        "Criar plano de retenção prioritário para top 10 lojas (risco de concentração)",
        "Analisar fatores de sucesso das lojas líderes: localização, categoria, estratégia",
        "Desenvolver programa de aceleração para lojas de médio desempenho",
        "Estabelecer SLA diferenciado e gerente de conta dedicado para top parceiros"
    ]
    
    return analysis, insights

def analyze_top_lojas_volume(df_top_volume):
    """Análise das lojas por volume de transações"""
    if len(df_top_volume) == 0:
        return "Dados insuficientes para análise.", []
    
    # Detecta colunas dinamicamente
    col_loja = 'nome_estabelecimento' if 'nome_estabelecimento' in df_top_volume.columns else 'Loja'
    col_volume = 'Número de Cupons' if 'Número de Cupons' in df_top_volume.columns else 'valor'
    
    # Se tiver tipo_cupom, agrupa
    if 'tipo_cupom' in df_top_volume.columns:
        df_agregado = df_top_volume.groupby(col_loja)[col_volume].sum().reset_index()
        df_agregado = df_agregado.sort_values(col_volume, ascending=False).head(10)
    else:
        df_agregado = df_top_volume.copy()
    
    total_transacoes = df_agregado[col_volume].sum()
    loja_lider = df_agregado.iloc[0][col_loja]
    transacoes_lider = df_agregado.iloc[0][col_volume]
    
    analysis = (
        f"Em volume de transações, '{loja_lider}' lidera com {transacoes_lider:,.0f} cupons. "
        "A análise de volume complementa a visão de receita, revelando lojas com alta "
        "frequência mas potencialmente baixo ticket médio."
    )
    
    insights = [
        "Cruzar dados de volume x receita para identificar oportunidades de aumento de ticket",
        "Lojas com alto volume e baixo ticket: criar estratégias de upsell",
        "Lojas com baixo volume e alto ticket: aumentar frequência com promoções",
        "Benchmark: estabelecer metas de volume por categoria de estabelecimento"
    ]
    
    return analysis, insights

def analyze_distribuicao_lojas(df_lojas_bairro, df_lojas_categoria):
    """Análise da distribuição geográfica e por categoria"""
    analysis_bairro = (
        "A distribuição de lojas por bairro revela concentração geográfica "
        "e oportunidades de expansão em áreas com alta demanda mas baixa cobertura."
    )
    
    analysis_categoria = (
        "A distribuição por categoria de estabelecimento permite avaliar "
        "diversificação do portfólio e identificar gaps no mix de parceiros."
    )
    
    insights_bairro = [
        "Mapear bairros com alto tráfego de usuários mas poucas lojas parceiras",
        "Criar programa de expansão direcionado para bairros sub-atendidos",
        "Analisar densidade de lojas vs densidade populacional por região"
    ]
    
    insights_categoria = [
        "Identificar categorias sub-representadas no portfólio de parceiros",
        "Desenvolver estratégia de aquisição focada em categorias de alto potencial",
        "Avaliar performance por categoria para priorizar esforços comerciais"
    ]
    
    return (analysis_bairro, insights_bairro), (analysis_categoria, insights_categoria)

def analyze_cupons_tipo(df_tipos):
    """Análise dos tipos de cupons"""
    if len(df_tipos) == 0:
        return "Dados insuficientes para análise.", []
    
    # Debug
    print(f"DEBUG analyze_cupons_tipo - Colunas disponíveis: {df_tipos.columns.tolist()}")
    print(f"DEBUG analyze_cupons_tipo - Primeiras linhas:\n{df_tipos.head()}")
    
    # Detecta colunas dinamicamente
    if 'tipo_cupom' in df_tipos.columns:
        col_tipo = 'tipo_cupom'
    elif 'Tipo' in df_tipos.columns:
        col_tipo = 'Tipo'
    else:
        col_tipo = 'Tipo de Cupom'
    
    if 'Número de Cupons' in df_tipos.columns:
        col_cupons = 'Número de Cupons'
    elif 'valor' in df_tipos.columns:
        col_cupons = 'valor'
    else:
        col_cupons = 'Receita Total'
    
    if 'Receita Total' in df_tipos.columns:
        col_receita = 'Receita Total'
    elif 'valor' in df_tipos.columns:
        col_receita = 'valor'
    else:
        col_receita = col_cupons
    
    total_cupons = df_tipos[col_cupons].sum()
    total_receita = df_tipos[col_receita].sum()
    tipo_mais_usado = df_tipos.iloc[0][col_tipo]
    cupons_tipo = df_tipos.iloc[0][col_cupons]
    receita_tipo = df_tipos.iloc[0][col_receita]
    
    analysis = (
        f"O tipo '{tipo_mais_usado}' domina com {cupons_tipo:,.0f} cupons "
        f"({(cupons_tipo/total_cupons*100):.1f}%) e R$ {receita_tipo:,.2f} em receita "
        f"({(receita_tipo/total_receita*100):.1f}%). A análise por tipo de cupom "
        "revela a eficácia de diferentes estratégias promocionais."
    )
    
    insights = [
        "Calcular ROI por tipo de cupom: custo de desconto vs incremento de transações",
        "Testar novos tipos de cupons em segmentos específicos (A/B testing)",
        "Otimizar mix de cupons baseado em margem e volume de cada tipo",
        "Criar cupons dinâmicos que se ajustam ao comportamento do usuário"
    ]
    
    return analysis, insights

def analyze_cupons_valor(df_valores):
    """Análise da distribuição de valores de cupons"""
    if len(df_valores) == 0:
        return "Dados insuficientes para análise.", []
    
    total_receita = df_valores['Receita Total'].sum()
    faixa_lider = df_valores.iloc[0]['Faixa de Valor']
    receita_faixa = df_valores.iloc[0]['Receita Total']
    percent = (receita_faixa / total_receita * 100) if total_receita > 0 else 0
    
    analysis = (
        f"A faixa de valor '{faixa_lider}' concentra {percent:.1f}% da receita total. "
        "A distribuição por faixas de valor revela padrões de consumo e sensibilidade "
        "a diferentes níveis de desconto."
    )
    
    insights = [
        "Analisar elasticidade-preço: impacto de diferentes valores de desconto no volume",
        "Otimizar faixas de valor para maximizar receita total (volume x margem)",
        "Criar estratégias diferenciadas por faixa: baixo valor (frequência) x alto valor (aquisição)",
        "Implementar precificação dinâmica baseada em perfil do usuário e momento"
    ]
    
    return analysis, insights

def analyze_correlacao_valor_repasse(correlacao, n_pontos):
    """Análise da correlação entre valor do cupom e repasse"""
    if correlacao is None:
        return "Dados insuficientes para calcular correlação.", []
    
    if correlacao > 0.9:
        forca = "muito forte"
    elif correlacao > 0.7:
        forca = "forte"
    elif correlacao > 0.5:
        forca = "moderada"
    elif correlacao > 0.3:
        forca = "fraca"
    else:
        forca = "muito fraca"
    
    analysis = (
        f"A correlação de {correlacao:.3f} entre valor do cupom e repasse MoneyBR "
        f"é classificada como {forca}. Com {n_pontos:,} pontos analisados, "
        "esta relação valida a estrutura de precificação e permite projeções confiáveis."
    )
    
    insights = [
        f"Correlação {forca} ({correlacao:.3f}) valida modelo de repasse proporcional ao valor",
        "Monitorar desvios da correlação esperada para identificar anomalias operacionais",
        "Utilizar modelo de regressão para projetar receitas baseadas em volume de cupons",
        "Avaliar se estrutura de repasse está otimizada ou pode ser ajustada"
    ]
    
    return analysis, insights

def analyze_tendencias_por_tipo(correlacoes_por_tipo):
    """Análise das tendências de correlação por tipo de cupom"""
    if not correlacoes_por_tipo:
        return "Dados insuficientes para análise.", []
    
    tipo_maior_corr = max(correlacoes_por_tipo.items(), key=lambda x: x[1])[0]
    tipo_menor_corr = min(correlacoes_por_tipo.items(), key=lambda x: x[1])[0]
    
    analysis = (
        f"As correlações variam por tipo de cupom: '{tipo_maior_corr}' apresenta "
        f"maior correlação enquanto '{tipo_menor_corr}' apresenta menor. "
        "Esta variação sugere comportamentos distintos de usuários e estruturas "
        "de repasse diferenciadas por tipo."
    )
    
    insights = [
        "Tipos com alta correlação: maior previsibilidade, bons para projeções",
        "Tipos com baixa correlação: investigar fatores externos que influenciam repasse",
        "Considerar estruturas de repasse diferenciadas por tipo de cupom",
        "Utilizar análise por tipo para segmentar estratégias de pricing"
    ]
    
    return analysis, insights

def analyze_saude_financeira(kpis):
    """Análise geral da saúde financeira"""
    margem = kpis.get('margem_operacional', 0)
    ticket_medio = kpis.get('ticket_medio', 0)
    cupons_capturados = kpis.get('cupons_capturados', 0)
    
    if margem > 0.25:
        status_margem = "excelente"
        acao_margem = "Manter estrutura atual e avaliar investimentos em crescimento"
    elif margem > 0.15:
        status_margem = "saudável"
        acao_margem = "Monitorar custos operacionais para preservar margem"
    elif margem > 0.10:
        status_margem = "adequada"
        acao_margem = "Buscar eficiências operacionais para melhorar margem"
    else:
        status_margem = "crítica"
        acao_margem = "Reavaliar estrutura de custos e repasse urgentemente"
    
    analysis = (
        f"A margem operacional de {margem*100:.1f}% é considerada {status_margem}. "
        f"Com {cupons_capturados:,} cupons e ticket médio de R$ {ticket_medio:.2f}, "
        "a empresa apresenta fundamentos sólidos para crescimento sustentável."
    )
    
    insights = [
        f"Margem {status_margem}: {acao_margem}",
        "Estabelecer metas financeiras trimestrais: receita, margem, ticket médio",
        "Implementar dashboard de KPIs financeiros com alertas automáticos",
        "Realizar análise de sensibilidade: impacto de variações em volume e margem"
    ]
    
    return analysis, insights

def get_recommendations_cfo():
    """Recomendações estratégicas gerais para o CFO"""
    return [
        "Diversificação de Receita: Reduzir dependência dos top parceiros expandindo base",
        "Otimização de Margem: Buscar 20-25% de margem operacional através de eficiências",
        "Aumento de Ticket Médio: Estratégias de upsell podem incrementar 15-20% sem custos adicionais",
        "Gestão de Concentração: Top 20% lojas geram 80% receita - criar plano de mitigação de risco",
        "Pricing Dinâmico: Implementar modelo de precificação variável por tipo/categoria/horário",
        "Análise Preditiva: Utilizar correlações para projeções financeiras mais precisas",
        "Controle de Custos: Automatizar processos para reduzir custo operacional por transação",
        "Capital de Giro: Monitorar ciclo de caixa e negociar prazos favoráveis com parceiros",
        "Métricas de Performance: Acompanhar LTV/CAC, churn rate e payback period por cohort",
        "Investimentos: Priorizar alocação de capital em iniciativas com maior ROI comprovado"
    ]

def calculate_financial_projections(receita_atual, margem_atual, taxa_crescimento_mensal=0.05):
    """Calcula projeções financeiras"""
    projecoes = {
        '3_meses': receita_atual * ((1 + taxa_crescimento_mensal) ** 3),
        '6_meses': receita_atual * ((1 + taxa_crescimento_mensal) ** 6),
        '12_meses': receita_atual * ((1 + taxa_crescimento_mensal) ** 12)
    }
    
    return {
        'receita_projetada': projecoes,
        'repasse_projetado': {k: v * margem_atual for k, v in projecoes.items()},
        'taxa_crescimento': taxa_crescimento_mensal
    }
