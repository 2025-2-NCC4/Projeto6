from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        # Caminho relativo para a logo
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'Frontend', 'assets', 'mbr_branco.png')
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.cell(30, 10, 'Relatório MoneyBR', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_chart(self, chart_path, width=190):
        self.image(chart_path, x = self.get_x(), y = self.get_y(), w = width)
        self.ln(10)

    def add_two_charts(self, chart_path1, chart_path2, width=90):
        self.image(chart_path1, x = self.get_x(), y = self.get_y(), w = width)
        self.image(chart_path2, x = self.get_x() + width + 10, y = self.get_y(), w = width)
        self.ln(width)
    def ln(self, h = None):
        super().ln(h)