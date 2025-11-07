"""
Módulo para construir PDFs completos com insights para CEO e CFO
"""

import os
from Backend.pdf_generator_enhanced import PDFEnhanced
from Backend import ceo_insights, cfo_insights


def build_ceo_pdf(filtros, dataframes, chart_paths, temp_dir):
    """
    Constrói um PDF completo para o CEO com insights estratégicos
    
    Args:
        filtros: dict com estabelecimentos, categorias, bairros selecionados
        dataframes: dict com todos os dataframes necessários
        chart_paths: dict com caminhos dos gráficos salvos
        temp_dir: diretório temporário para salvar gráficos
    
    Returns:
        pdf_output em bytes
    """
    pdf = PDFEnhanced(report_type="CEO")
    pdf.alias_nb_pages()
    
    # ========== PÁGINA 1: SUMÁRIO EXECUTIVO ==========
    pdf.add_page()
    
    summary = ceo_insights.get_executive_summary_ceo(filtros)
    pdf.add_section_title(summary['titulo'])
    pdf.add_text(summary['descricao'])
    pdf.ln(3)
    
    pdf.add_subsection_title("Filtros Aplicados")
    for filtro in summary['filtros']:
        pdf.add_bullet_point(filtro)
    
    # ========== PÁGINA 2: VOLUMETRIAS GERAIS ==========
    pdf.add_page()
    pdf.add_section_title("Volumetrias Gerais")
    
    # Top Estabelecimentos
    if 'df_top_estabelecimentos' in dataframes and 'fig_estab' in chart_paths:
        analysis, insights = ceo_insights.analyze_top_estabelecimentos(dataframes['df_top_estabelecimentos'])
        pdf.add_chart_with_analysis(
            chart_paths['fig_estab'],
            "Top 10 Estabelecimentos por Transações",
            analysis,
            insights
        )
    
    # Top Categorias
    if 'df_top_categorias' in dataframes and 'fig_cat' in chart_paths:
        if pdf.get_y() > 200:
            pdf.add_page()
        analysis, insights = ceo_insights.analyze_top_categorias(dataframes['df_top_categorias'])
        pdf.add_chart_with_analysis(
            chart_paths['fig_cat'],
            "Top 10 Categorias Mais Utilizadas",
            analysis,
            insights
        )
    
    # ========== PÁGINA 3: ANÁLISE GEOGRÁFICA ==========
    pdf.add_page()
    pdf.add_section_title("Analise Geografica")
    
    # Bairros
    if 'df_top_bairros' in dataframes and 'fig_bairros' in chart_paths:
        analysis, insights = ceo_insights.analyze_top_bairros(dataframes['df_top_bairros'])
        pdf.add_chart_with_analysis(
            chart_paths['fig_bairros'],
            "Top 10 Bairros por Número de Transações",
            analysis,
            insights
        )
    
    # Cupons
    if 'df_cupons' in dataframes and 'fig_cupons' in chart_paths:
        if pdf.get_y() > 200:
            pdf.add_page()
        analysis, insights = ceo_insights.analyze_cupons(dataframes['df_cupons'])
        pdf.add_chart_with_analysis(
            chart_paths['fig_cupons'],
            "Tipos de Cupons Mais Utilizados",
            analysis,
            insights
        )
    
    # ========== PÁGINA 4: PERFIL DOS CLIENTES ==========
    pdf.add_page()
    pdf.add_section_title("Perfil dos Clientes")
    
    if 'df_base' in dataframes:
        analysis, insights = ceo_insights.analyze_perfil_clientes(dataframes['df_base'])
        pdf.add_text("Visão Geral:", bold=True)
        pdf.add_text(analysis)
        pdf.ln(3)
        pdf.add_text("Oportunidades Estratégicas:", bold=True)
        for insight in insights:
            pdf.add_bullet_point(insight)
    
    # Cidade de Residência
    if 'df_cidade_res' in dataframes and 'fig_cidade_res' in chart_paths:
        pdf.ln(5)
        analysis, insights = ceo_insights.analyze_cidades_residencia(dataframes['df_cidade_res'])
        pdf.add_chart_with_analysis(
            chart_paths['fig_cidade_res'],
            "Top 10 Cidades de Residência",
            analysis,
            insights
        )
    
    # ========== PÁGINA 5: DADOS DEMOGRÁFICOS - RESIDÊNCIA ==========
    if 'fig_bairro_res' in chart_paths:
        pdf.add_page()
        pdf.add_section_title("Dados Demograficos - Residencia")
        
        if 'df_bairro_res' in dataframes:
            analysis, insights = ceo_insights.analyze_bairros_residencia(dataframes['df_bairro_res'])
            pdf.add_chart_with_analysis(
                chart_paths['fig_bairro_res'],
                "Top 10 Bairros de Residência",
                analysis,
                insights
            )
    
    # ========== PÁGINA 6: DADOS DEMOGRÁFICOS - TRABALHO ==========
    if 'fig_cidade_trab' in chart_paths or 'fig_bairro_trab' in chart_paths:
        pdf.add_page()
        pdf.add_section_title("Dados Demograficos - Trabalho")
        
        # Cidade de Trabalho
        if 'df_cidade_trab' in dataframes and 'fig_cidade_trab' in chart_paths:
            analysis, insights = ceo_insights.analyze_cidades_trabalho(dataframes['df_cidade_trab'])
            pdf.add_chart_with_analysis(
                chart_paths['fig_cidade_trab'],
                "Top 10 Cidades de Trabalho",
                analysis,
                insights
            )
        
        # Bairro de Trabalho
        if 'df_bairro_trab' in dataframes and 'fig_bairro_trab' in chart_paths:
            if pdf.get_y() > 200:
                pdf.add_page()
            analysis, insights = ceo_insights.analyze_bairros_trabalho(dataframes['df_bairro_trab'])
            pdf.add_chart_with_analysis(
                chart_paths['fig_bairro_trab'],
                "Top 10 Bairros de Trabalho",
                analysis,
                insights
            )
    
    # ========== PÁGINA 7: PERFIL DEMOGRÁFICO DETALHADO ==========
    pdf.add_page()
    pdf.add_section_title("Perfil Demografico Detalhado")
    
    # Idade e Gasto - lado a lado
    if 'fig_idade' in chart_paths and 'fig_gasto' in chart_paths:
        analysis_idade, analysis_gasto = ceo_insights.analyze_idade_gasto(
            dataframes.get('df_idade'), 
            dataframes.get('df_gasto')
        )
        pdf.add_two_charts_with_analysis(
            chart_paths['fig_idade'], "Distribuição de Idade",  analysis_idade,
            chart_paths['fig_gasto'], "Gasto Médio dos Clientes", analysis_gasto
        )
    
    # Sexo e Modelo - lado a lado
    if 'fig_sexo' in chart_paths and 'fig_modelo' in chart_paths:
        if pdf.get_y() > 180:
            pdf.add_page()
        analysis_sexo, analysis_modelo = ceo_insights.analyze_sexo_modelo(
            dataframes.get('df_sexo'),
            dataframes.get('df_modelo')
        )
        pdf.add_two_charts_with_analysis(
            chart_paths['fig_sexo'], "Distribuição por Sexo", analysis_sexo,
            chart_paths['fig_modelo'], "Modelos de Smartphone", analysis_modelo
        )
    
    # ========== PÁGINA 8: AVENIDA PAULISTA ==========
    if 'df_paulista' in dataframes:
        pdf.add_page()
        pdf.add_section_title("Detalhamento: Avenida Paulista")
        
        analysis, insights = ceo_insights.analyze_avenida_paulista(dataframes['df_paulista'])
        pdf.add_text(analysis)
        pdf.ln(3)
        pdf.add_text("Oportunidades Identificadas:", bold=True)
        for insight in insights:
            pdf.add_bullet_point(insight)
        
        # Horário e Local
        if 'fig_horario' in chart_paths and 'fig_local' in chart_paths:
            pdf.ln(5)
            analysis_horario, analysis_local = ceo_insights.analyze_horario_local_paulista(
                dataframes.get('df_horario'),
                dataframes.get('df_local')
            )
            pdf.add_two_charts_with_analysis(
                chart_paths['fig_horario'], "Pedestres por Faixa de Horário", analysis_horario,
                chart_paths['fig_local'], "Pedestres por Local", analysis_local
            )
    
    # ========== PÁGINA FINAL: RECOMENDAÇÕES ESTRATÉGICAS ==========
    pdf.add_page()
    pdf.add_section_title("Recomendacoes Estrategicas")
    
    recommendations = ceo_insights.get_recommendations_ceo()
    pdf.add_text(
        "Com base na análise completa dos dados, recomendamos as seguintes ações prioritárias "
        "para maximizar o crescimento e a eficiência operacional da MoneyBR:",
        size=11
    )
    pdf.ln(5)
    
    for i, rec in enumerate(recommendations, 1):
        # Separa título do corpo
        parts = rec.split(': ', 1)
        if len(parts) == 2:
            titulo, descricao = parts
            pdf.add_text(f"{i}. {titulo}:", bold=True, size=11)
            pdf.set_x(20)
            pdf.add_text(descricao, size=10)
            pdf.ln(2)
        else:
            pdf.add_bullet_point(rec)
    
    return pdf.output(dest='S')


def build_cfo_pdf(filtros, dataframes, chart_paths, temp_dir, kpis=None):
    """
    Constrói um PDF completo para o CFO com insights financeiros
    
    Args:
        filtros: dict com filtros aplicados
        dataframes: dict com todos os dataframes necessários
        chart_paths: dict com caminhos dos gráficos salvos
        temp_dir: diretório temporário para salvar gráficos
        kpis: dict com KPIs principais (opcional)
    
    Returns:
        pdf_output em bytes
    """
    pdf = PDFEnhanced(report_type="CFO")
    pdf.alias_nb_pages()
    
    # KPIs padrão se não fornecidos
    if kpis is None:
        kpis = {
            'receita_total': 0,
            'receita_moneybr': 0,
            'margem_operacional': 0,
            'ticket_medio': 0,
            'cupons_capturados': 0,
            'usuarios_ativos': 0,
            'lojas_ativas': 0
        }
    
    # ========== PÁGINA 1: SUMÁRIO EXECUTIVO ==========
    pdf.add_page()
    
    summary = cfo_insights.get_executive_summary_cfo(kpis, filtros)
    pdf.add_section_title(summary['titulo'])
    pdf.add_text(summary['descricao'])
    pdf.ln(3)
    
    pdf.add_subsection_title("Filtros Aplicados")
    for filtro in summary['filtros']:
        pdf.add_bullet_point(filtro)
    
    # Métricas principais
    pdf.ln(5)
    pdf.add_subsection_title("Métricas Principais")
    metrics_display = {
        'Receita Total': f"R$ {kpis['receita_total']:,.2f}",
        'Repasse MoneyBR': f"R$ {kpis['receita_moneybr']:,.2f}",
        'Margem Operacional': f"{kpis['margem_operacional']*100:.1f}%",
        'Ticket Médio': f"R$ {kpis['ticket_medio']:.2f}",
        'Cupons Capturados': f"{kpis['cupons_capturados']:,}",
        'Usuários Ativos': f"{kpis['usuarios_ativos']:,}"
    }
    pdf.add_metric_box(metrics_display)
    
    # Análise da Volumetria
    pdf.ln(5)
    analysis, insights = cfo_insights.analyze_volumetria_financeira(kpis)
    pdf.add_text("Análise da Volumetria Financeira:", bold=True)
    pdf.add_text(analysis, size=10)
    pdf.ln(3)
    pdf.add_text("Insights Estratégicos:", bold=True)
    for insight in insights:
        pdf.add_bullet_point(insight)
    
    # ========== PÁGINA 2: ANÁLISE DE RECEITA OPERACIONAL ==========
    pdf.add_page()
    pdf.add_section_title("Estrutura de Receitas")
    
    if 'receita_liquida' in kpis:
        analysis, insights = cfo_insights.analyze_receita_operacional(
            kpis['receita_total'], 
            kpis['receita_moneybr'],
            kpis['receita_liquida']
        )
        pdf.add_text(analysis)
        pdf.ln(3)
        pdf.add_text("Recomendações:", bold=True)
        for insight in insights:
            pdf.add_bullet_point(insight)
    
    # ========== DETALHAMENTO DOS LOJISTAS ==========
    if 'fig_repasse_dia' in chart_paths or 'fig_cupons_dia' in chart_paths:
        pdf.add_page()
        pdf.add_section_title("Detalhamento dos Lojistas")
        
        # Informação sobre os filtros de loja
        lojas_filtradas = filtros.get('lojas', [])
        if lojas_filtradas and len(lojas_filtradas) > 0:
            if len(lojas_filtradas) == 1:
                pdf.add_text(f"Análise específica da loja: {lojas_filtradas[0]}", bold=True, size=11)
            else:
                pdf.add_text(f"Análise de {len(lojas_filtradas)} lojas selecionadas", bold=True, size=11)
        else:
            pdf.add_text("Análise de todas as lojas do portfólio", bold=True, size=11)
        
        pdf.ln(3)
        
        # Gráficos de repasse e cupons por dia lado a lado
        if 'fig_repasse_dia' in chart_paths and 'fig_cupons_dia' in chart_paths:
            analysis_repasse = (
                "O gráfico de repasse diário MoneyBR em julho de 2025 revela padrões sazonais "
                "e picos de atividade. Dias com maior repasse indicam campanhas bem-sucedidas "
                "ou eventos que impulsionaram transações."
            )
            analysis_cupons = (
                "O volume de cupons capturados por dia complementa a visão financeira, "
                "mostrando a frequência de utilização do serviço. A correlação entre volume "
                "de cupons e repasse indica a efetividade das estratégias promocionais."
            )
            pdf.add_two_charts_with_analysis(
                chart_paths['fig_repasse_dia'], "Repasse MoneyBR por Dia", analysis_repasse,
                chart_paths['fig_cupons_dia'], "Cupons Capturados por Dia", analysis_cupons
            )
        elif 'fig_repasse_dia' in chart_paths:
            analysis = (
                "O repasse diário MoneyBR ao longo do mês demonstra a consistência "
                "de receita e permite identificar dias de alta performance para replicação."
            )
            pdf.add_chart_with_analysis(
                chart_paths['fig_repasse_dia'],
                "Repasse MoneyBR por Dia",
                analysis,
                [
                    "Identificar dias de pico para entender fatores que impulsionam receita",
                    "Criar campanhas direcionadas para dias de baixa performance",
                    "Monitorar sazonalidade para planejamento de caixa"
                ]
            )
        elif 'fig_cupons_dia' in chart_paths:
            analysis = (
                "O volume diário de cupons capturados indica o nível de engajamento "
                "dos usuários e a efetividade das estratégias de ativação."
            )
            pdf.add_chart_with_analysis(
                chart_paths['fig_cupons_dia'],
                "Cupons Capturados por Dia",
                analysis,
                [
                    "Aumentar frequência de uso através de notificações estratégicas",
                    "Identificar dias de baixa atividade para ações promocionais",
                    "Estabelecer metas diárias baseadas em histórico de performance"
                ]
            )
    
    # ========== ANÁLISE POR LOJAS ==========
    pdf.add_page()
    pdf.add_section_title("Performance por Estabelecimento")
    
    # Top Lojas por Receita
    if 'df_top_lojas_receita' in dataframes and 'fig_lojas_receita' in chart_paths:
        analysis, insights = cfo_insights.analyze_top_lojas_receita(dataframes['df_top_lojas_receita'])
        pdf.add_chart_with_analysis(
            chart_paths['fig_lojas_receita'],
            "Top 10 Lojas por Receita",
            analysis,
            insights
        )
    
    # ========== PÁGINA 3: ANÁLISE DE VOLUME ==========
    if 'df_top_lojas_volume' in dataframes and 'fig_lojas_volume' in chart_paths:
        pdf.add_page()
        pdf.add_section_title("Analise de Volume de Transacoes")
        
        analysis, insights = cfo_insights.analyze_top_lojas_volume(dataframes['df_top_lojas_volume'])
        pdf.add_chart_with_analysis(
            chart_paths['fig_lojas_volume'],
            "Top 10 Lojas por Número de Cupons",
            analysis,
            insights
        )
    
    # ========== PÁGINA 4: ANÁLISE DE CUPONS ==========
    pdf.add_page()
    pdf.add_section_title("Analise de Cupons e Promocoes")
    
    # Informação sobre filtros de tipos de cupom
    tipos_filtrados = filtros.get('tipos_cupom', [])
    if tipos_filtrados and len(tipos_filtrados) > 0:
        pdf.add_text(f"Análise focada em: {', '.join(tipos_filtrados)}", bold=True, size=11)
    else:
        pdf.add_text("Análise de todos os tipos de cupons disponíveis", bold=True, size=11)
    
    pdf.ln(5)
    
    # Cupons por Tipo (opcional - se houver gráfico específico)
    if 'df_cupons_tipo' in dataframes and 'fig_cupons_tipo' in chart_paths:
        analysis, insights = cfo_insights.analyze_cupons_tipo(dataframes['df_cupons_tipo'])
        pdf.add_chart_with_analysis(
            chart_paths['fig_cupons_tipo'],
            "Análise por Tipo de Cupom",
            analysis,
            insights
        )
    elif 'df_cupons_tipo' in dataframes:
        # Se não houver gráfico mas houver dados, mostra apenas análise textual
        analysis, insights = cfo_insights.analyze_cupons_tipo(dataframes['df_cupons_tipo'])
        pdf.add_text(analysis, size=10)
        pdf.ln(3)
        for insight in insights:
            pdf.add_bullet_point(insight)
        pdf.ln(5)
    
    # Top 10 Lojas por Cupons (gráfico de barras empilhado por tipo)
    if 'fig_top_lojas' in chart_paths:
        if pdf.get_y() > 200:
            pdf.add_page()
        
        analysis_lojas_cupons = (
            "A análise de receita por loja e tipo de cupom revela quais estabelecimentos "
            "são mais receptivos a diferentes estratégias promocionais. Esta segmentação "
            "permite otimizar o mix de cupons oferecidos a cada parceiro."
        )
        pdf.add_chart_with_analysis(
            chart_paths['fig_top_lojas'],
            "Top 10 Lojas por Valor de Cupons",
            analysis_lojas_cupons,
            [
                "Personalizar ofertas de cupons baseado no perfil de cada loja",
                "Lojas com alto volume de cupons premium: foco em retenção VIP",
                "Lojas com diversidade de tipos: parceiros estratégicos para testes",
                "Estabelecer metas de mix de cupons por categoria de estabelecimento"
            ]
        )
    
    # Top 10 Bairros por Cupons
    if 'fig_top_bairros' in chart_paths:
        if pdf.get_y() > 200:
            pdf.add_page()
        
        analysis_bairros_cupons = (
            "A distribuição geográfica de cupons por bairro identifica regiões de alta "
            "atividade e oportunidades de expansão. Bairros com alta concentração de "
            "um tipo específico de cupom indicam perfis demográficos distintos."
        )
        pdf.add_chart_with_analysis(
            chart_paths['fig_top_bairros'],
            "Top 10 Bairros por Valor de Cupons",
            analysis_bairros_cupons,
            [
                "Mapear perfil socioeconômico de bairros para direcionar tipos de cupom",
                "Criar campanhas geoloc alizadas para bairros de alto potencial",
                "Identificar bairros sub-explorados para expansão de parceiros",
                "Analisar densidade de cupons vs densidade populacional"
            ]
        )
    
    # Cupons por Valor
    if 'df_cupons_valor' in dataframes and 'fig_cupons_valor' in chart_paths:
        if pdf.get_y() > 200:
            pdf.add_page()
        analysis, insights = cfo_insights.analyze_cupons_valor(dataframes['df_cupons_valor'])
        pdf.add_chart_with_analysis(
            chart_paths['fig_cupons_valor'],
            "Distribuição por Faixa de Valor",
            analysis,
            insights
        )
    
    # ========== PÁGINA 6: CORRELAÇÕES ==========
    if 'fig_correlacao' in chart_paths:
        pdf.add_page()
        pdf.add_section_title("Analise de Correlacoes")
        
        if 'correlacao_valor' in dataframes and 'n_pontos' in dataframes:
            analysis, insights = cfo_insights.analyze_correlacao_valor_repasse(
                dataframes['correlacao_valor'],
                dataframes['n_pontos']
            )
            pdf.add_chart_with_analysis(
                chart_paths['fig_correlacao'],
                "Correlação: Valor do Cupom vs Repasse MoneyBR",
                analysis,
                insights
            )
    
    # ========== PÁGINA 7: SAÚDE FINANCEIRA ==========
    pdf.add_page()
    pdf.add_section_title("Saude Financeira e Eficiencia")
    
    # Análise de Saúde Financeira
    analysis, insights = cfo_insights.analyze_saude_financeira(kpis)
    pdf.add_text(analysis)
    pdf.ln(3)
    pdf.add_text("Indicadores e Ações:", bold=True)
    for insight in insights:
        pdf.add_bullet_point(insight)
    
    # Análise de Eficiência Operacional
    if all(k in kpis for k in ['cupons_capturados', 'usuarios_ativos', 'lojas_ativas']):
        pdf.ln(5)
        pdf.add_subsection_title("Eficiência Operacional")
        analysis, insights = cfo_insights.analyze_eficiencia_operacional(
            kpis['cupons_capturados'],
            kpis['usuarios_ativos'],
            kpis['lojas_ativas'],
            kpis['receita_total'],
            kpis['receita_moneybr']
        )
        pdf.add_text(analysis)
        pdf.ln(3)
        pdf.add_text("Oportunidades de Melhoria:", bold=True)
        for insight in insights:
            pdf.add_bullet_point(insight)
    
    # ========== PÁGINA FINAL: RECOMENDAÇÕES ESTRATÉGICAS ==========
    pdf.add_page()
    pdf.add_section_title("Recomendacoes Estrategicas")
    
    recommendations = cfo_insights.get_recommendations_cfo()
    pdf.add_text(
        "Com base na analise financeira completa, recomendamos as seguintes acoes para "
        "otimizar rentabilidade e eficiencia de custos:",
        size=11
    )
    pdf.ln(5)
    
    for i, rec in enumerate(recommendations, 1):
        parts = rec.split(': ', 1)
        if len(parts) == 2:
            titulo, descricao = parts
            pdf.add_text(f"{i}. {titulo}:", bold=True, size=11)
            pdf.set_x(20)
            pdf.add_text(descricao, size=10)
            pdf.ln(2)
        else:
            pdf.add_bullet_point(rec)
    
    return pdf.output(dest='S')
