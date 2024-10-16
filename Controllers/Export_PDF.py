from fpdf import FPDF
from PIL import Image
import os

class Criar_PDF():
    def __init__(self):
        self.fpdf = FPDF()

    def gerar_pdf(self, tx_final, tabela, natureza, risco, linha, n_linha, prazo, nome_cli, nome_ger, nome_pa, num_pa, email):
        self.fpdf.add_page()

        current_dir = os.path.abspath(os.curdir)
        original_logo_path = os.path.join(current_dir, 'Images', 'Logo.png')
        
        # Converter a imagem para um formato compatível mantendo a transparência
        temp_logo_path = os.path.join(current_dir, 'Images', 'Logo_temp.png')

        # Abrir a imagem original e mantê-la em modo RGBA para preservar a transparência
        with Image.open(original_logo_path) as img:
            # Verificar se a imagem está em modo RGBA para suportar a transparência
            if img.mode != 'RGBA':
                img = img.convert("RGBA")
            # Salvar a imagem temporária preservando a transparência
            img.save(temp_logo_path, 'PNG')

        # Incluir logo no PDF
        logo_width = 50
        page_width = self.fpdf.w
        x_centered = (page_width - logo_width) / 2

        # Adicionar a imagem convertida ao PDF
        self.fpdf.image(temp_logo_path, x=x_centered, y=8, w=logo_width)

        # Adicionar o restante do conteúdo ao PDF
        self.fpdf.set_font('Times', 'B', 16)
        self.fpdf.cell(200, 12, '', ln=True, align='C')
        self.fpdf.cell(200, 12, '', ln=True, align='C')
        self.fpdf.cell(200, 13, 'Simulação de Taxa Padrão Pré-Precificada', ln=True, align='C')
        self.fpdf.cell(200, 11, f'Linha de Crédito: {linha}', ln=True, align='C')

        self.fpdf.set_font('Times', '', 12)
        self.fpdf.ln(10)
        self.fpdf.cell(0, 10, f'Cooperado: {nome_cli}', ln=True)
        self.fpdf.cell(0, 10, f'Tipo de Tabela: {tabela}', ln=True)
        self.fpdf.cell(0, 10, f'Natureza: {natureza}', ln=True)
        self.fpdf.cell(0, 10, f'Risco: {risco}', ln=True)
        self.fpdf.cell(0, 10, f'Linha de Crédito: {linha}', ln=True)
        self.fpdf.cell(0, 10, f'Número da Linha: {n_linha}', ln=True)
        self.fpdf.cell(0, 10, f'Prazo: {prazo}', ln=True)
        self.fpdf.cell(0, 10, f'Taxa Final (a.m): {tx_final}%', ln=True)
        self.fpdf.cell(0, 10, f'Taxa Final (a.a): {round(100 * (((1 + (float(tx_final) / 100)) ** 12) - 1), 2)}%', ln=True)
        self.fpdf.cell(0, 10, "", ln=True)
        self.fpdf.cell(0, 10, f"Gerente: {nome_ger}", ln=True)
        self.fpdf.cell(0, 10, f"Agência: {nome_pa} | {num_pa}", ln=True)
        self.fpdf.cell(0, 10, f"Entre em Contato com seu gerente: {email}", ln=True)
        
        # Salvar PDF
        pdf_path = f'Export/{email}/Simulação_{nome_cli[:20]}.pdf'
        self.fpdf.output(pdf_path)
        
        # Retornar o caminho do PDF gerado
        return pdf_path

    def gerar_pdf_com_desc(self, tx_desc, tabela, natureza, risco, linha, n_linha, prazo, nome_cli, nome_ger, nome_pa, num_pa, email):
        self.fpdf.add_page()

        current_dir = os.path.abspath(os.curdir)
        original_logo_path = os.path.join(current_dir, 'Images', 'Logo.png')
        
        # Converter a imagem para um formato compatível mantendo a transparência
        temp_logo_path = os.path.join(current_dir, 'Images', 'Logo_temp.png')

        # Abrir a imagem original e mantê-la em modo RGBA para preservar a transparência
        with Image.open(original_logo_path) as img:
            # Verificar se a imagem está em modo RGBA para suportar a transparência
            if img.mode != 'RGBA':
                img = img.convert("RGBA")
            # Salvar a imagem temporária preservando a transparência
            img.save(temp_logo_path, 'PNG')

        # Incluir logo no PDF
        logo_width = 50
        page_width = self.fpdf.w
        x_centered = (page_width - logo_width) / 2

        # Adicionar a imagem convertida ao PDF
        self.fpdf.image(temp_logo_path, x=x_centered, y=8, w=logo_width)

        # Adicionar o restante do conteúdo ao PDF
        self.fpdf.set_font('Arial', 'B', 16)
        self.fpdf.cell(200, 12, '', ln=True, align='C')
        self.fpdf.cell(200, 12, '', ln=True, align='C')
        self.fpdf.cell(200, 13, 'Simulação de Taxa com Solicitação de Desconto', ln=True, align='C')
        self.fpdf.cell(200, 11, f'Linha de Crédito: {linha}', ln=True, align='C')

        self.fpdf.set_font('Arial', '', 12)
        self.fpdf.ln(10)
        self.fpdf.cell(0, 10, f'Cooperado: {nome_cli}', ln=True)
        self.fpdf.cell(0, 10, f'Tipo de Tabela: {tabela}', ln=True)
        self.fpdf.cell(0, 10, f'Natureza: {natureza}', ln=True)
        self.fpdf.cell(0, 10, f'Risco: {risco}', ln=True)
        self.fpdf.cell(0, 10, f'Linha de Crédito: {linha}', ln=True)
        self.fpdf.cell(0, 10, f'Número da Linha: {n_linha}', ln=True)
        self.fpdf.cell(0, 10, f'Prazo: {prazo}', ln=True)
        self.fpdf.cell(0, 10, f'Taxa Final (a.m): {tx_desc}%', ln=True)
        self.fpdf.cell(0, 10, f'Taxa Final (a.a): {round(100 * (((1 + (float(tx_desc) / 100)) ** 12) - 1), 2)}%', ln=True)
        self.fpdf.cell(0, 10, "", ln=True)
        self.fpdf.cell(0, 10, f"Gerente: {nome_ger}", ln=True)
        self.fpdf.cell(0, 10, f"Agência: {nome_pa} | {num_pa}", ln=True)
        self.fpdf.cell(0, 10, f"Entre em Contato com seu gerente: {email}", ln=True)
        
        # Salvar PDF
        pdf_path = f'Export/{email}/Simulação_com_desc_{nome_cli[:20]}.pdf'
        self.fpdf.output(pdf_path)
        
        # Retornar o caminho do PDF gerado
        return pdf_path