"""
Funções auxiliares para geração de PDFs aprimorados para CEO e CFO
"""
import os
import pandas as pd
import numpy as np

def generate_ceo_pdf_enhanced(pdf, charts, filtros, df_data, temp_dir):
    """
    Gera PDF aprimorado para CEO com análises e insights
    
    Args:
        pdf: Instância do PDFEnhanced
        charts: Dicionário com os gráficos gerados
        filtros: Dicionário com filtros aplicados
        df_data: Dicionário com DataFrames processados
        temp_dir: Diretório temporário para salvar imagens
    """
    from Backend.ceo_insights import (
        get_executive_summary_ceo,
        analyze_top_estabelecimentos,
        analyze_top_categorias,
        analyze_top_bairros,
        analyze_cupons,
        analyze_perfil_clientes,
        analyze_cidades_residencia,
        analyze_bairros_residencia,
        analyze_cidades_trabalho,
        analyze_bairros_trabalho,
        analyze_idade_gasto,
        analyze_sexo_modelo,
        analyze_avenida_paulista,
        analyze_horario_local_paulista,
        get_recommendations_ceo
    )
    
    # Página de capa
    pdf.add_page()
    
    # Sumário executivo
    summary = get_executive_summary_ceo(filtros)
    pdf.add_section_title(summary['titulo'], '')
    pdf.add_text(summary['descricao'], size=11)
    pdf.ln(3)
    
    # Filtros aplicados em destaque
    pdf.add_highlight_box(
        'Filtros Aplicados',
        '\n'.join(summary['filtros'])
    )
    
    # Métricas principais do relatório
    if 'metricas' in df_data:
        pdf.add_metric_box(df_data['metricas'])
    
    # ==== VOLUMETRIAS GERAIS ====
    pdf.add_page()
    pdf.add_section_title('Volumetrias Gerais')
    
    # Análise de estabelecimentos
    if 'df_top_estab' in df_data and not df_data['df_top_estab'].empty:
        analysis, insights = analyze_top_estabelecimentos(df_data['df_top_estab'])
        chart_path = os.path.join(temp_dir, "fig_estab.png")
        if charts.get('fig_estab'):
            try:
                charts['fig_estab'].write_image(chart_path)
                pdf.add_chart_with_analysis(
                    chart_path,
                    'Top Estabelecimentos por Transações',
                    analysis,
                    insights
                )
            except Exception as e:
                print(f"Erro ao gerar gráfico estabelecimentos: {e}")
    
    # Análise de categorias
    if 'df_top_cat' in df_data and not df_data['df_top_cat'].empty:
        analysis, insights = analyze_top_categorias(df_data['df_top_cat'])
        chart_path = os.path.join(temp_dir, "fig_cat.png")
        if charts.get('fig_cat'):
            try:
                charts['fig_cat'].write_image(chart_path)
                pdf.add_chart_with_analysis(
                    chart_path,
                    'Top Categorias por Transações',
                    analysis,
                    insights
                )
            except Exception as e:
                print(f"Erro ao gerar gráfico categorias: {e}")
    
    # Análise de bairros e cupons lado a lado
    if charts.get('fig_bairros') and charts.get('fig_cupons'):
        if 'df_top_bairros' in df_data and 'df_top_cupons' in df_data:
            analysis_bairro, insights_b = analyze_top_bairros(df_data['df_top_bairros'])
            analysis_cupom, insights_c = analyze_cupons(df_data['df_top_cupons'])
            
            chart_path1 = os.path.join(temp_dir, "fig_bairros.png")
            chart_path2 = os.path.join(temp_dir, "fig_cupons.png")
            
            try:
                charts['fig_bairros'].write_image(chart_path1)
                charts['fig_cupons'].write_image(chart_path2)
                pdf.add_two_charts_with_analysis(
                    chart_path1, 'Bairros - Transações', analysis_bairro,
                    chart_path2, 'Tipos de Cupons', analysis_cupom
                )
                
                # Insights em lista
                pdf.add_text("Insights Estratégicos - Bairros:", bold=True)
                for insight in insights_b[:3]:  # Top 3
                    pdf.add_bullet_point(insight)
                    
                pdf.ln(3)
                pdf.add_text("Insights Estratégicos - Cupons:", bold=True)
                for insight in insights_c[:3]:  # Top 3
                    pdf.add_bullet_point(insight)
                    
            except Exception as e:
                print(f"Erro ao gerar gráficos duplos: {e}")
    
    # ==== PERFIL DOS CLIENTES ====
    pdf.add_page()
    pdf.add_section_title('Perfil dos Clientes')
    
    if 'df_base' in df_data:
        analysis, insights = analyze_perfil_clientes(df_data['df_base'])
        pdf.add_text(analysis, size=11)
        pdf.ln(2)
        for insight in insights[:4]:
            pdf.add_bullet_point(insight)
    
    # ==== DADOS DEMOGRÁFICOS ====
    pdf.add_page()
    pdf.add_section_title('Dados Demográficos')
    
    # Cidades e bairros de residência
    if charts.get('fig_cidade_res') and charts.get('fig_bairro_res'):
        if 'df_cidade_res' in df_data and 'df_bairro_res' in df_data:
            analysis_cidade, insights_cid = analyze_cidades_residencia(df_data['df_cidade_res'])
            analysis_bairro, insights_bai = analyze_bairros_residencia(df_data['df_bairro_res'])
            
            chart_path1 = os.path.join(temp_dir, "fig_cidade_res.png")
            chart_path2 = os.path.join(temp_dir, "fig_bairro_res.png")
            
            try:
                charts['fig_cidade_res'].write_image(chart_path1)
                charts['fig_bairro_res'].write_image(chart_path2)
                pdf.add_two_charts_with_analysis(
                    chart_path1, 'Residência - Cidades', analysis_cidade,
                    chart_path2, 'Residência - Bairros', analysis_bairro
                )
            except Exception as e:
                print(f"Erro ao gerar gráficos residência: {e}")
    
    # Cidades e bairros de trabalho
    if charts.get('fig_cidade_trab') and charts.get('fig_bairro_trab'):
        if 'df_cidade_trab' in df_data and 'df_bairro_trab' in df_data:
            analysis_cidade, insights_cid = analyze_cidades_trabalho(df_data['df_cidade_trab'])
            analysis_bairro, insights_bai = analyze_bairros_trabalho(df_data['df_bairro_trab'])
            
            chart_path1 = os.path.join(temp_dir, "fig_cidade_trab.png")
            chart_path2 = os.path.join(temp_dir, "fig_bairro_trab.png")
            
            try:
                charts['fig_cidade_trab'].write_image(chart_path1)
                charts['fig_bairro_trab'].write_image(chart_path2)
                pdf.add_two_charts_with_analysis(
                    chart_path1, 'Trabalho - Cidades', analysis_cidade,
                    chart_path2, 'Trabalho - Bairros', analysis_bairro
                )
            except Exception as e:
                print(f"Erro ao gerar gráficos trabalho: {e}")
    
    # ==== AVENIDA PAULISTA ====
    if 'df_paulista' in df_data and not df_data['df_paulista'].empty:
        pdf.add_page()
        pdf.add_section_title('Detalhamento: Avenida Paulista')
        
        analysis, insights = analyze_avenida_paulista(df_data['df_paulista'])
        pdf.add_text(analysis, size=11)
        pdf.ln(2)
        for insight in insights:
            pdf.add_bullet_point(insight)
        
        # Gráficos da Paulista
        if charts.get('fig_horario') and charts.get('fig_local'):
            analysis_horario, analysis_local = analyze_horario_local_paulista(None, None)
            
            chart_path1 = os.path.join(temp_dir, "fig_horario.png")
            chart_path2 = os.path.join(temp_dir, "fig_local.png")
            
            try:
                charts['fig_horario'].write_image(chart_path1)
                charts['fig_local'].write_image(chart_path2)
                pdf.add_two_charts_with_analysis(
                    chart_path1, 'Distribuição por Horário', analysis_horario,
                    chart_path2, 'Principais Locais', analysis_local
                )
            except Exception as e:
                print(f"Erro ao gerar gráficos Paulista: {e}")
    
    # ==== RECOMENDAÇÕES ESTRATÉGICAS ====
    pdf.add_page()
    pdf.add_section_title('Recomendações Estratégicas')
    
    recommendations = get_recommendations_ceo()
    pdf.add_text(
        'Com base na análise dos dados apresentados, seguem as principais '
        'recomendações estratégicas para impulsionar o crescimento da MoneyBR:',
        size=11
    )
    pdf.ln(3)
    
    for i, rec in enumerate(recommendations, 1):
        pdf.add_text(f'{i}. {rec}', bold=False, size=11)
        pdf.ln(2)
    
    return pdf


def generate_cfo_pdf_enhanced(pdf, charts, filtros, kpis, df_data, temp_dir):
    """
    Gera PDF aprimorado para CFO com análises financeiras e insights
    
    Args:
        pdf: Instância do PDFEnhanced
        charts: Dicionário com os gráficos gerados
        filtros: Dicionário com filtros aplicados
        kpis: Dicionário com KPIs financeiros
        df_data: Dicionário com DataFrames processados
        temp_dir: Diretório temporário para salvar imagens
    """
    from Backend.cfo_insights import (
        get_executive_summary_cfo,
        analyze_volumetria_financeira,
        analyze_receita_operacional,
        analyze_eficiencia_operacional,
        analyze_top_lojas_receita,
        analyze_top_lojas_volume,
        analyze_distribuicao_lojas,
        analyze_cupons_tipo,
        analyze_cupons_valor,
        analyze_correlacao_valor_repasse,
        analyze_tendencias_por_tipo,
        analyze_saude_financeira,
        get_recommendations_cfo,
        calculate_financial_projections
    )
    
    # Página de capa
    pdf.add_page()
    
    # Sumário executivo
    summary = get_executive_summary_cfo(kpis, filtros)
    pdf.add_section_title(summary['titulo'])
    pdf.add_text(summary['descricao'], size=11)
    pdf.ln(3)
    
    # Filtros aplicados
    pdf.add_highlight_box(
        'Filtros Aplicados',
        '\n'.join(summary['filtros'])
    )
    
    # KPIs principais em destaque
    kpi_display = {
        'Receita Total': f"R$ {kpis.get('receita_total', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        'Repasse MoneyBR': f"R$ {kpis.get('receita_moneybr', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
        'Margem Op.': f"{kpis.get('margem_operacional', 0)*100:.1f}%",
        'Ticket Médio': f"R$ {kpis.get('ticket_medio', 0):.2f}".replace('.', ','),
        'Cupons': f"{kpis.get('cupons_capturados', 0):,}".replace(',', '.'),
        'Usuários': f"{kpis.get('usuarios_ativos', 0):,}".replace(',', '.')
    }
    pdf.add_metric_box(kpi_display)
    
    # ==== ANÁLISE FINANCEIRA GERAL ====
    pdf.add_page()
    pdf.add_section_title('Análise Financeira Geral')
    
    # Volumetria financeira
    analysis, insights = analyze_volumetria_financeira(kpis)
    pdf.add_subsection_title('Volumetria Financeira')
    pdf.add_text(analysis, size=11)
    pdf.ln(2)
    for insight in insights:
        pdf.add_bullet_point(insight)
    
    # Receita operacional
    pdf.ln(5)
    analysis, insights = analyze_receita_operacional(
        kpis.get('receita_total', 0),
        kpis.get('receita_moneybr', 0),
        kpis.get('receita_liquida', 0)
    )
    pdf.add_subsection_title('Estrutura de Receitas')
    pdf.add_text(analysis, size=11)
    pdf.ln(2)
    for insight in insights[:3]:
        pdf.add_bullet_point(insight)
    
    # Eficiência operacional
    pdf.ln(5)
    analysis, insights = analyze_eficiencia_operacional(
        kpis.get('cupons_capturados', 0),
        kpis.get('usuarios_ativos', 0),
        kpis.get('lojas_ativas', 0),
        kpis.get('receita_total', 0),
        kpis.get('receita_moneybr', 0)
    )
    pdf.add_subsection_title('Eficiência Operacional')
    pdf.add_text(analysis, size=11)
    pdf.ln(2)
    for insight in insights[:3]:
        pdf.add_bullet_point(insight)
    
    # ==== DETALHAMENTO DOS LOJISTAS ====
    pdf.add_page()
    pdf.add_section_title('Detalhamento dos Lojistas')
    
    # Top lojas por receita
    if 'df_top_lojas_receita' in df_data and not df_data['df_top_lojas_receita'].empty:
        analysis, insights = analyze_top_lojas_receita(df_data['df_top_lojas_receita'])
        if charts.get('fig'):
            chart_path = os.path.join(temp_dir, "fig_top_lojas_receita.png")
            try:
                charts['fig'].write_image(chart_path)
                pdf.add_chart_with_analysis(
                    chart_path,
                    'Top Lojas por Receita',
                    analysis,
                    insights[:4]
                )
            except Exception as e:
                print(f"Erro ao gerar gráfico top lojas receita: {e}")
    
    # Top lojas por volume
    if 'df_top_lojas_volume' in df_data and not df_data['df_top_lojas_volume'].empty:
        analysis, insights = analyze_top_lojas_volume(df_data['df_top_lojas_volume'])
        if charts.get('fig2'):
            chart_path = os.path.join(temp_dir, "fig_top_lojas_volume.png")
            try:
                charts['fig2'].write_image(chart_path)
                pdf.add_chart_with_analysis(
                    chart_path,
                    'Top Lojas por Volume',
                    analysis,
                    insights[:4]
                )
            except Exception as e:
                print(f"Erro ao gerar gráfico top lojas volume: {e}")
    
    # ==== DETALHAMENTO DOS CUPONS ====
    pdf.add_page()
    pdf.add_section_title('Detalhamento dos Cupons')
    
    # Análise por tipo de cupom
    if 'df_cupons_tipo' in df_data and not df_data['df_cupons_tipo'].empty:
        analysis, insights = analyze_cupons_tipo(df_data['df_cupons_tipo'])
        pdf.add_subsection_title('Análise por Tipo de Cupom')
        pdf.add_text(analysis, size=11)
        pdf.ln(2)
        for insight in insights[:3]:
            pdf.add_bullet_point(insight)
    
    # Gráficos de cupons
    if charts.get('fig_l') and charts.get('fig_b'):
        chart_path1 = os.path.join(temp_dir, "fig_cupons_loja.png")
        chart_path2 = os.path.join(temp_dir, "fig_cupons_bairro.png")
        
        try:
            charts['fig_l'].write_image(chart_path1)
            charts['fig_b'].write_image(chart_path2)
            pdf.add_two_charts_with_analysis(
                chart_path1, 'Cupons por Loja', 'Distribuição de valor dos cupons entre as top lojas parceiras.',
                chart_path2, 'Cupons por Bairro', 'Concentração geográfica dos cupons utilizados.'
            )
        except Exception as e:
            print(f"Erro ao gerar gráficos cupons: {e}")
    
    # ==== CORRELAÇÕES E TENDÊNCIAS ====
    pdf.add_page()
    pdf.add_section_title('Correlações e Tendências')
    
    # Análise de correlação
    if 'correlacao' in df_data:
        analysis, insights = analyze_correlacao_valor_repasse(
            df_data['correlacao'],
            df_data.get('n_pontos_correlacao', 0)
        )
        pdf.add_subsection_title('Correlação Valor x Repasse')
        pdf.add_text(analysis, size=11)
        pdf.ln(2)
        for insight in insights[:3]:
            pdf.add_bullet_point(insight)
        
        # Gráfico de correlação
        if charts.get('fig_corr'):
            chart_path = os.path.join(temp_dir, "fig_correlacao.png")
            try:
                charts['fig_corr'].write_image(chart_path)
                pdf.ln(3)
                pdf.image(chart_path, x=10, y=pdf.get_y(), w=190)
                pdf.ln(110)
            except Exception as e:
                print(f"Erro ao gerar gráfico correlação: {e}")
    
    # ==== SAÚDE FINANCEIRA E PROJEÇÕES ====
    pdf.add_page()
    pdf.add_section_title('Saúde Financeira e Projeções')
    
    analysis, insights = analyze_saude_financeira(kpis)
    pdf.add_text(analysis, size=11)
    pdf.ln(2)
    for insight in insights:
        pdf.add_bullet_point(insight)
    
    # Projeções
    pdf.ln(5)
    pdf.add_subsection_title('Projeções de Crescimento')
    projections = calculate_financial_projections(
        kpis.get('receita_total', 0),
        kpis.get('margem_operacional', 0),
        0.05  # 5% crescimento mensal
    )
    
    proj_text = (
        f"Considerando uma taxa de crescimento mensal de {projections['taxa_crescimento']*100:.1f}%, "
        "as projeções de receita são:\n\n"
        f"3 meses: R$ {projections['receita_projetada']['3_meses']:,.2f}\n"
        f"6 meses: R$ {projections['receita_projetada']['6_meses']:,.2f}\n"
        f"12 meses: R$ {projections['receita_projetada']['12_meses']:,.2f}"
    )
    pdf.add_text(proj_text.replace(',', 'X').replace('.', ',').replace('X', '.'), size=10)
    
    # ==== RECOMENDAÇÕES ESTRATÉGICAS ====
    pdf.add_page()
    pdf.add_section_title('Recomendações Estratégicas')
    
    recommendations = get_recommendations_cfo()
    pdf.add_text(
        'Com base na análise financeira e operacional, seguem as principais '
        'recomendações estratégicas para otimizar a performance da MoneyBR:',
        size=11
    )
    pdf.ln(3)
    
    for i, rec in enumerate(recommendations, 1):
        pdf.add_text(f'{i}. {rec}', bold=False, size=11)
        pdf.ln(2)
    
    return pdf
