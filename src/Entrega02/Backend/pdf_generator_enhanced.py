from fpdf import FPDF
from datetime import datetime
import os

class PDFEnhanced(FPDF):
    def __init__(self, report_type="CEO"):
        super().__init__()
        self.report_type = report_type
        
    def header(self):
        # Logo usando caminho relativo
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'Frontend', 'assets', 'mbr_branco.png')
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 8, 33)
        
        # Título principal
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 112, 49)  # Verde MoneyBR
        self.cell(80)
        self.cell(30, 10, f'Relatório Executivo - {self.report_type}', 0, 0, 'C')
        
        # Data de geração
        self.set_font('Arial', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.ln(15)
        self.cell(0, 5, f'Gerado em: {datetime.now().strftime("%d/%m/%Y às %H:%M")}', 0, 0, 'R')
        
        # Linha separadora
        self.ln(8)
        self.set_draw_color(0, 112, 49)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(0, 112, 49)
        self.set_line_width(0.3)
        self.line(10, self.get_y() - 2, 200, self.get_y() - 2)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'MoneyBR - Página {self.page_no()}/{{nb}}', 0, 0, 'C')

    def add_section_title(self, title, icon=""):
        """Adiciona um título de seção destacado"""
        self.ln(5)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 112, 49)
        # Ignora o icon para evitar problemas com emojis
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_draw_color(0, 112, 49)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
        self.set_text_color(0, 0, 0)

    def add_subsection_title(self, title):
        """Adiciona um subtítulo de seção"""
        self.ln(3)
        self.set_font('Arial', 'B', 13)
        self.set_text_color(0, 70, 30)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def add_text(self, text, bold=False, size=11, align='L'):
        """Adiciona texto formatado"""
        if bold:
            self.set_font('Arial', 'B', size)
        else:
            self.set_font('Arial', '', size)
        self.multi_cell(0, 6, text, 0, align)
        self.ln(2)

    def add_bullet_point(self, text):
        """Adiciona um ponto com marcador"""
        self.set_font('Arial', '', 9)
        x_start = self.get_x()
        
        # Marcador
        self.set_text_color(0, 112, 49)
        self.cell(5, 5, chr(149), 0, 0)  # Bullet point
        self.set_text_color(0, 0, 0)
        
        # Texto
        self.set_x(x_start + 7)
        self.multi_cell(0, 5, text)
        self.ln(0.5)

    def add_highlight_box(self, title, content, bg_color=(240, 248, 242)):
        """Adiciona uma caixa destacada com informações"""
        self.ln(3)
        
        # Desenha retângulo de fundo
        x = self.get_x()
        y = self.get_y()
        self.set_fill_color(bg_color[0], bg_color[1], bg_color[2])
        self.rect(x, y, 190, 20, 'F')
        
        # Título da caixa
        self.set_text_color(0, 112, 49)
        self.set_xy(x + 5, y + 3)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 6, title, 0, 1)
        
        # Conteúdo da caixa
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 11)
        self.set_x(x + 5)
        self.multi_cell(180, 5, content)
        
        self.ln(5)
        self.set_text_color(0, 0, 0)

    def add_metric_box(self, metrics_dict):
        """Adiciona caixas de métricas lado a lado"""
        self.ln(3)
        x_start = 10
        y_start = self.get_y()
        box_width = 60
        box_height = 18
        spacing = 5
        
        col = 0
        row = 0
        for label, value in metrics_dict.items():
            x = x_start + (box_width + spacing) * col
            y = y_start + (box_height + spacing) * row
            
            # Fundo da métrica
            self.set_fill_color(245, 250, 246)
            self.rect(x, y, box_width, box_height, 'F')
            
            # Borda
            self.set_draw_color(0, 112, 49)
            self.set_line_width(0.3)
            self.rect(x, y, box_width, box_height, 'D')
            
            # Label
            self.set_xy(x + 2, y + 2)
            self.set_font('Arial', 'B', 9)
            self.set_text_color(100, 100, 100)
            self.cell(box_width - 4, 5, label, 0, 0, 'C')
            
            # Valor
            self.set_xy(x + 2, y + 9)
            self.set_font('Arial', 'B', 12)
            self.set_text_color(0, 112, 49)
            self.cell(box_width - 4, 5, str(value), 0, 0, 'C')
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        self.set_xy(x_start, y_start + (row + 1) * (box_height + spacing) + 5)
        self.set_text_color(0, 0, 0)

    def add_chart_with_analysis(self, chart_path, title, analysis, insights=None, width=150):
        """Adiciona gráfico com título e análise detalhada"""
        # Verifica se precisa de nova página
        if self.get_y() > 200:
            self.add_page()
            
        self.add_subsection_title(title)
        
        # Adiciona o gráfico com tamanho controlado
        y_before = self.get_y()
        try:
            # Usa apenas width para manter proporção original
            self.image(chart_path, x=15, y=y_before, w=width)
            # Calcula altura real baseada na proporção da imagem
            # Gráficos Plotly geralmente tem proporção de 0.65 a 0.75
            estimated_height = width * 0.70
            # Move cursor para DEPOIS do gráfico + margem de segurança
            self.set_y(y_before + estimated_height + 10)
        except Exception as e:
            self.set_y(y_before + 40)
            self.add_text("[Grafico nao disponivel]", size=10)
        
        # Análise do gráfico
        self.add_text("Analise:", bold=True, size=10)
        self.add_text(analysis, size=9)
        
        # Insights estratégicos
        if insights:
            self.ln(2)
            self.add_text("Insights Estrategicos:", bold=True, size=10)
            for insight in insights:
                self.add_bullet_point(insight)
        
        self.ln(4)

    def add_two_charts_with_analysis(self, chart_path1, title1, analysis1, 
                                      chart_path2, title2, analysis2, width=80):
        """Adiciona dois gráficos lado a lado com análises"""
        if self.get_y() > 180:
            self.add_page()
        
        y_start = self.get_y()
        
        # Primeiro gráfico - apenas width, mantém proporção
        try:
            self.image(chart_path1, x=12, y=y_start, w=width)
        except:
            pass
        
        # Segundo gráfico - apenas width, mantém proporção
        try:
            self.image(chart_path2, x=108, y=y_start, w=width)
        except:
            pass
        
        # Calcula altura estimada e move cursor
        estimated_height = width * 0.70
        self.set_y(y_start + estimated_height + 10)
        
        # Análises lado a lado
        self.ln(2)
        
        # Análise 1
        self.set_font('Arial', 'B', 9)
        self.set_xy(12, self.get_y())
        self.multi_cell(80, 4, title1)
        
        y_after_title1 = self.get_y()
        
        # Análise 2
        self.set_xy(108, y_start + estimated_height + 12)
        self.multi_cell(80, 4, title2)
        
        # Textos das análises
        self.set_font('Arial', '', 8)
        
        # Análise 1
        self.set_xy(12, y_after_title1 + 1)
        self.multi_cell(80, 3.5, analysis1)
        
        y_after_first = self.get_y()
        
        # Análise 2
        self.set_xy(108, y_start + estimated_height + 12 + 8)
        self.multi_cell(80, 3.5, analysis2)
        
        # Ajusta Y para o maior
        y_after_second = self.get_y()
        self.set_y(max(y_after_first, y_after_second) + 4)

    # Métodos para compatibilidade com código existente
    def chapter_title(self, title):
        """Mantido para compatibilidade"""
        self.add_section_title(title)

    def chapter_body(self, body):
        """Mantido para compatibilidade"""
        self.add_text(body)

    def add_chart(self, chart_path, width=150):
        """Mantido para compatibilidade"""
        if self.get_y() > 220:
            self.add_page()
        y_pos = self.get_y()
        try:
            self.image(chart_path, x=15, y=y_pos, w=width)
            estimated_height = width * 0.70
            self.set_y(y_pos + estimated_height + 10)
        except:
            self.add_text("[Grafico nao disponivel]")
            self.ln(10)

    def add_two_charts(self, chart_path1, chart_path2, width=80):
        """Mantido para compatibilidade"""
        if self.get_y() > 200:
            self.add_page()
        y_pos = self.get_y()
        try:
            self.image(chart_path1, x=12, y=y_pos, w=width)
        except:
            pass
        try:
            self.image(chart_path2, x=108, y=y_pos, w=width)
        except:
            pass
        estimated_height = width * 0.70
        self.set_y(y_pos + estimated_height + 10)
        
    def ln(self, h=None):
        super().ln(h)
