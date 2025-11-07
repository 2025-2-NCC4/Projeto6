"""
Módulo com análises e insights estratégicos para o relatório CEO
"""

def get_executive_summary_ceo(filtros):
    """Retorna o sumário executivo baseado nos filtros aplicados"""
    filtros_text = []
    if filtros.get('estabelecimentos'):
        filtros_text.append(f"Estabelecimentos: {', '.join(filtros['estabelecimentos'])}")
    else:
        filtros_text.append("Estabelecimentos: Todos")
        
    if filtros.get('categorias'):
        filtros_text.append(f"Categorias: {', '.join(filtros['categorias'])}")
    else:
        filtros_text.append("Categorias: Todas")
        
    if filtros.get('bairros'):
        filtros_text.append(f"Bairros: {', '.join(filtros['bairros'])}")
    else:
        filtros_text.append("Bairros: Todos")
    
    return {
        'titulo': 'Sumário Executivo',
        'descricao': (
            'Este relatório apresenta uma análise estratégica do desempenho da MoneyBR, '
            'com foco em volumetrias operacionais, perfil de clientes e análise geográfica. '
            'Os dados foram processados com os seguintes filtros aplicados.'
        ),
        'filtros': filtros_text
    }

def analyze_top_estabelecimentos(df_top):
    """Análise estratégica dos estabelecimentos"""
    total_transacoes = df_top['Número de transações'].sum()
    top_3_percent = (df_top.head(3)['Número de transações'].sum() / total_transacoes * 100) if total_transacoes > 0 else 0
    
    analysis = (
        f"Os {len(df_top)} principais estabelecimentos concentram {total_transacoes:,} transações. "
        f"Os 3 estabelecimentos líderes representam {top_3_percent:.1f}% do volume total, "
        "indicando forte concentração de demanda em poucos parceiros estratégicos."
    )
    
    insights = [
        "Priorizar relacionamento com top 3 estabelecimentos para garantir continuidade operacional",
        "Identificar práticas de sucesso dos líderes para replicar em outros parceiros",
        "Avaliar expansão de parceria com estabelecimentos de médio volume para diversificar riscos",
        "Criar programa de incentivos para estabelecimentos com potencial de crescimento"
    ]
    
    return analysis, insights

def analyze_top_categorias(df_cat):
    """Análise estratégica das categorias"""
    total_transacoes = df_cat['Número de transações'].sum()
    categoria_lider = df_cat.iloc[0]['Categoria'] if len(df_cat) > 0 else "N/A"
    percent_lider = (df_cat.iloc[0]['Número de transações'] / total_transacoes * 100) if len(df_cat) > 0 and total_transacoes > 0 else 0
    
    analysis = (
        f"A categoria '{categoria_lider}' lidera com {percent_lider:.1f}% do total de transações. "
        f"A distribuição entre {len(df_cat)} categorias principais revela oportunidades "
        "de expansão em segmentos com menor penetração mas alto potencial de mercado."
    )
    
    insights = [
        f"Fortalecer estratégia de marketing na categoria líder: {categoria_lider}",
        "Mapear categorias emergentes com crescimento acelerado para investimento prioritário",
        "Desenvolver campanhas específicas para categorias de baixo volume mas alto ticket médio",
        "Analisar sazonalidade por categoria para otimizar recursos de marketing"
    ]
    
    return analysis, insights

def analyze_top_bairros(df_bairros):
    """Análise estratégica dos bairros"""
    total_transacoes = df_bairros['Número de transações'].sum()
    bairro_lider = df_bairros.iloc[0]['Bairro'] if len(df_bairros) > 0 else "N/A"
    
    analysis = (
        f"O bairro '{bairro_lider}' apresenta maior concentração de transações, "
        "indicando alta densidade de usuários ativos e estabelecimentos parceiros. "
        "A análise geográfica revela clusters de alta performance que podem ser replicados."
    )
    
    insights = [
        "Expandir cobertura de estabelecimentos em bairros de alto volume",
        "Realizar estudos demográficos dos bairros líderes para identificar perfil ideal",
        "Criar zonas de expansão prioritária baseadas no desempenho dos top bairros",
        "Desenvolver parcerias locais com associações comerciais dos bairros estratégicos"
    ]
    
    return analysis, insights

def analyze_cupons(df_cupons):
    """Análise estratégica dos cupons"""
    total_cupons = df_cupons['Número de transações'].sum()
    tipo_mais_usado = df_cupons.iloc[0]['Tipo de cupom'] if len(df_cupons) > 0 else "N/A"
    percent_tipo = (df_cupons.iloc[0]['Número de transações'] / total_cupons * 100) if len(df_cupons) > 0 and total_cupons > 0 else 0
    
    analysis = (
        f"O tipo de cupom '{tipo_mais_usado}' domina com {percent_tipo:.1f}% das transações. "
        "A distribuição de tipos de cupons reflete a estratégia de incentivos "
        "e a preferência dos usuários por diferentes modalidades de desconto."
    )
    
    insights = [
        f"Otimizar disponibilidade do tipo de cupom mais popular: {tipo_mais_usado}",
        "Testar novos tipos de cupons em segmentos de baixa adesão",
        "Analisar ROI por tipo de cupom para otimizar investimento em promoções",
        "Criar programa de cupons personalizados baseado no comportamento do usuário"
    ]
    
    return analysis, insights

def analyze_perfil_clientes(df_base):
    """Análise do perfil dos clientes"""
    total_clientes = len(df_base)
    
    analysis = (
        f"A base conta com {total_clientes:,} clientes cadastrados. "
        "A análise de perfil revela padrões demográficos e comportamentais "
        "essenciais para estratégias de segmentação e personalização."
    )
    
    insights = [
        "Segmentar comunicação por perfil demográfico para aumentar engajamento",
        "Criar jornadas personalizadas baseadas em comportamento de compra",
        "Identificar clientes de alto valor (high-value) para programa de fidelidade premium",
        "Desenvolver estratégias de reativação para clientes inativos"
    ]
    
    return analysis, insights

def analyze_cidades_residencia(df_cidades):
    """Análise das cidades de residência"""
    if len(df_cidades) == 0:
        return "Dados insuficientes para análise.", []
        
    # Tenta identificar a coluna correta
    col_cidade = None
    col_count = None
    
    if 'Cidade' in df_cidades.columns:
        col_cidade = 'Cidade'
        col_count = 'Número de clientes'
    elif 'cidade_residencial' in df_cidades.columns:
        col_cidade = 'cidade_residencial'
        col_count = 'count' if 'count' in df_cidades.columns else df_cidades.columns[1]
    else:
        # Assume primeira coluna é cidade, segunda é contagem
        col_cidade = df_cidades.columns[0]
        col_count = df_cidades.columns[1]
    
    total = df_cidades[col_count].sum()
    cidade_lider = df_cidades.iloc[0][col_cidade]
    percent_lider = (df_cidades.iloc[0][col_count] / total * 100) if total > 0 else 0
    
    analysis = (
        f"A cidade '{cidade_lider}' concentra {percent_lider:.1f}% da base de clientes. "
        "A distribuição geográfica de residência indica o alcance da plataforma "
        "e oportunidades de expansão regional."
    )
    
    insights = [
        "Concentrar esforços de marketing nas cidades com maior base de usuários",
        "Avaliar penetração de mercado por cidade (usuários MoneyBR vs população total)",
        "Identificar cidades com baixa penetração mas alto potencial de crescimento",
        "Desenvolver parcerias com estabelecimentos em novas cidades estratégicas"
    ]
    
    return analysis, insights

def analyze_bairros_residencia(df_bairros):
    """Análise dos bairros de residência"""
    analysis = (
        "A distribuição de clientes por bairro de residência revela padrões "
        "de concentração urbana e permite estratégias de geo-marketing mais eficientes."
    )
    
    insights = [
        "Criar campanhas regionalizadas por bairro para maior relevância",
        "Mapear correlação entre bairro de residência e locais de consumo",
        "Identificar gaps de cobertura em bairros de alta densidade populacional",
        "Desenvolver parcerias com estabelecimentos próximos aos bairros de alta concentração"
    ]
    
    return analysis, insights

def analyze_cidades_trabalho(df_cidades):
    """Análise das cidades de trabalho"""
    analysis = (
        "A análise de cidades de trabalho revela padrões de mobilidade urbana "
        "e identifica oportunidades para estabelecimentos em regiões comerciais."
    )
    
    insights = [
        "Priorizar parcerias com estabelecimentos em distritos comerciais e empresariais",
        "Desenvolver campanhas para horários de almoço em áreas corporativas",
        "Mapear fluxos de deslocamento casa-trabalho para otimizar oferta de cupons",
        "Criar promoções específicas para dias úteis em regiões empresariais"
    ]
    
    return analysis, insights

def analyze_bairros_trabalho(df_bairros):
    """Análise dos bairros de trabalho"""
    analysis = (
        "Os bairros de trabalho mais frequentes indicam hubs econômicos "
        "com alta circulação de potenciais usuários durante horário comercial."
    )
    
    insights = [
        "Expandir rede de estabelecimentos parceiros em bairros de alto fluxo corporativo",
        "Criar ofertas específicas para happy hour e almoços executivos",
        "Desenvolver programa de benefícios corporativos B2B para empresas locais",
        "Analisar potencial de estabelecimentos em rotas entre casa e trabalho"
    ]
    
    return analysis, insights

def analyze_idade_gasto(idade_data, gasto_data):
    """Análise combinada de idade e gasto médio"""
    analysis_idade = (
        "A distribuição etária da base revela o perfil geracional dos usuários, "
        "essencial para definir linguagem, canais de comunicação e tipos de oferta."
    )
    
    analysis_gasto = (
        "O gasto médio por cliente indica o potencial de receita e permite "
        "segmentação por valor para estratégias diferenciadas de retenção."
    )
    
    return analysis_idade, analysis_gasto

def analyze_sexo_modelo(sexo_data, modelo_data):
    """Análise de sexo e modelo de smartphone"""
    analysis_sexo = (
        "A distribuição por gênero permite personalização de ofertas e comunicação "
        "baseada em preferências e comportamentos de consumo diferenciados."
    )
    
    analysis_modelo = (
        "Os modelos de smartphone utilizados indicam poder aquisitivo e "
        "perfil tecnológico dos usuários, informações valiosas para segmentação."
    )
    
    return analysis_sexo, analysis_modelo

def analyze_avenida_paulista(df_paulista):
    """Análise específica da Avenida Paulista"""
    total_registros = len(df_paulista)
    
    analysis = (
        f"A Avenida Paulista apresenta {total_registros:,} registros de pedestres, "
        "representando um dos principais corredores comerciais com altíssimo "
        "potencial para aquisição de novos usuários e parcerias estratégicas."
    )
    
    insights = [
        "Intensificar presença de estabelecimentos parceiros ao longo da Avenida Paulista",
        "Criar campanhas de aquisição geo-localizadas para capturar pedestres",
        "Mapear horários de pico para otimizar exibição de ofertas",
        "Desenvolver parcerias com eventos e estabelecimentos âncora da região"
    ]
    
    return analysis, insights

def analyze_horario_local_paulista(horario_data, local_data):
    """Análise de horários e locais da Paulista"""
    analysis_horario = (
        "A distribuição por faixa de horário revela padrões de circulação "
        "e permite otimizar momento de envio de notificações e promoções."
    )
    
    analysis_local = (
        "Os locais com maior concentração de registros indicam pontos estratégicos "
        "para expansão de parcerias e ações de marketing in-loco."
    )
    
    return analysis_horario, analysis_local

def get_recommendations_ceo():
    """Recomendações estratégicas gerais para o CEO"""
    return [
        "Expansão Geográfica: Priorizar regiões com alta densidade de usuários e baixa penetração de estabelecimentos",
        "Otimização de Parcerias: Concentrar esforços nos top 20% estabelecimentos que geram 80% do volume",
        "Segmentação de Clientes: Desenvolver estratégias diferenciadas para clusters de alto, médio e baixo valor",
        "Inovação em Cupons: Testar novos formatos de incentivos baseados em comportamento e preferências",
        "Marketing Data-Driven: Utilizar insights demográficos e geográficos para campanhas hipersegmentadas",
        "Experiência Mobile: Investir em UX personalizada baseada no perfil do dispositivo e comportamento",
        "Análise Preditiva: Implementar modelos de churn e lifetime value para ações proativas",
        "Expansão B2B: Criar programa corporativo para empresas em regiões de alta concentração profissional"
    ]
