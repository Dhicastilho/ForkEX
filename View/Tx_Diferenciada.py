import streamlit as st
from Controllers.Sender import Sender_email
from Controllers.Export_PDF import Criar_PDF

class Taxa_Diferenciada():
    def __init__(self, tx, tabela, natureza, risco, linha, n_linha, prazo, nome):
        # Recebe a taxa simulada como argumento e define o valor máximo da taxa diferenciada
        self.tx_prec = tx
        self.tabela = tabela
        self.natureza = natureza
        self.risco = risco
        self.linha = linha
        self.n_linha = n_linha
        self.prazo = prazo
        self.nome = nome
        self.tx_minima = round(tx * 0.9, 2)
        self.tx_desconto = 0.00
        
    def gravar_valores(self):
        # Salvar valores na sessão do Streamlit
        st.session_state['taxa_desconto'] = self.tx_desconto
        
    def mostrar_pagina(self):
        """Exibe os componentes da página de solicitação de taxa diferenciada."""
        self.carregar_logo_e_titulo()
        self.exibir_taxas()
        self.carregar_corpo()
        self.carregar_rodape()

    def carregar_logo_e_titulo(self):
        """Carrega o logo e o título da página."""
        col1, col2 = st.columns([0.5, 2])
        col1.image('Images/Logo.png', width=100, use_column_width="always")
        col2.markdown("<h1 style='text-align: center; color: #C9D200;'>Solicitar Taxa Diferenciada</h1>", unsafe_allow_html=True)

    def exibir_taxas(self):
        """Exibe a taxa precificada e a taxa mínima permitida."""
        st.metric("Taxa Precificada (a.m)", f"{self.tx_prec}%")
        st.metric("Taxa Mínima Permitida (a.m)", f"{self.tx_minima}%")

    def carregar_range_taxa(self):
        """Inicia o input para o usuário solicitar a taxa diferenciada."""
        global tx_desconto
        tx_desconto = float(st.text_input("Taxa com Desconto (a.m)", value=self.tx_prec))

    def carregar_corpo(self):
        """Carrega o corpo da página, incluindo a solicitação da taxa diferenciada."""
        self.carregar_range_taxa()
        
        if tx_desconto >= self.tx_minima and tx_desconto <= self.tx_prec:
            self.gravar_valores()
            st.button("Solicitar Desconto de Taxa", on_click=self.processar_solicitacao)
        else:
            st.button("Solicitar Desconto de Taxa", disabled=True)
            
    def processar_solicitacao(self):
        """Processa a solicitação de taxa diferenciada e envia um e-mail."""
        caminho_pdf = self.gerar_exportacao_pdf()
        with open(caminho_pdf, "rb") as file:
            st.download_button('Baixar Arquivo', data=file, file_name=caminho_pdf)
                    
        self.enviar_email()
        st.success(f"Solicitação enviada com sucesso! Taxa solicitada: {tx_desconto}%")
    
    def campos_preenchidos(self):
        """Verifica se todos os campos necessários estão preenchidos."""
        return all([self.nome, self.tabela, self.natureza, self.risco, self.linha, self.n_linha, self.prazo])
    
    def enviar_email(self):
        """Envia o e-mail com a taxa diferenciada solicitada."""
        email = Sender_email(nome_cooperado=self.nome, linha=self.linha, taxa=self.tx_prec)
        email.enviar_com_desconto(tx_desconto)
          
    def gerar_exportacao_pdf(self):
        """Exporta a simulação para PDF."""
        if self.campos_preenchidos():
            with st.spinner("Gerando PDF..."):
                try:
                    caminho_pdf = self.exportar_pdf(tx_desconto, self.tabela, self.natureza, self.risco, self.linha, self.n_linha, self.prazo, self.nome)
                    st.success("PDF gerado com sucesso!")
                    
                    return caminho_pdf
                except Exception as e:
                    st.error(f"Ocorreu um erro ao gerar o PDF: {e}")
    
    @staticmethod
    def exportar_pdf(tx_desc, tabela, natureza, risco, linha, n_linha, prazo, nome):
        pdf = Criar_PDF()
        print(tx_desc)
        return pdf.gerar_pdf_com_desc(tx_desc=tx_desc, tabela=tabela, natureza=natureza, risco=risco, linha=linha, n_linha=n_linha, prazo=prazo, nome=nome)
    
    def carregar_rodape(self):
        """Carrega o rodapé da página."""
        col1, col2, col3= st.columns([1, 3, 1])
        col2.markdown("<p style='text-align: center; color: #C9D200; font-size: 20px;'></p>", unsafe_allow_html=True)
        col2.markdown("<p style='text-align: center; color: #C9D200; font-size: 20px;'>Desenvolvido pela equipe de BI no departamento de Controladoria!</p>", unsafe_allow_html=True)


