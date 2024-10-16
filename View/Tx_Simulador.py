import streamlit as st
import pandas as pd
from Controllers.Export_PDF import Criar_PDF
from Controllers.Sender import Sender_email
from View.Tx_Diferenciada import Taxa_Diferenciada

class Simulador():
    def __init__(self):
        """Inicia a interface da página."""
        # Inicializa as variáveis
        self.tx_final = 0.0
        self.tabela = ""
        self.natureza = ""
        self.risco = ""
        self.linha = ""
        self.n_linha = ""
        self.prazo = ""
        self.nome = ""

        # Inicializa a tela ativa no estado da sessão (tela padrão: Simulação)
        if 'tela_ativa' not in st.session_state:
            st.session_state['tela_ativa'] = 'simulador'

    def mostrar_simulador(self):
        self.carregar_logo_e_titulo()
        self.inicializar_componentes()
        self.main()
            
    def gravar_valores(self):
        # Salvar valores na sessão do Streamlit
        st.session_state['taxa'] = self.tx_final
        st.session_state['tabela'] = self.tabela
        st.session_state['natureza'] = self.natureza
        st.session_state['risco'] = self.risco
        st.session_state['linha'] = self.linha
        st.session_state['n_linha'] = self.n_linha
        st.session_state['prazo'] = self.prazo
        st.session_state['nome'] = self.nome
        
    def carregar_logo_e_titulo(self):
        """Carrega o logo e o título da página."""
        col1, col2, col3 = st.columns([0.4, 0.1, 1.5])
        col1.image('Images/Logo.png', width=100, use_column_width="always")
        col3.markdown("<h1 style='text-align: center; color: #C9D200;'>Taxas para a Concessão de Crédito</h1>", unsafe_allow_html=True)

    def inicializar_componentes(self):
        """Inicializa componentes da interface como o input de nome e tabela."""
        self.nome = st.text_input("Nome do Cooperado", placeholder="Insira aqui o nome do cooperado")
        with st.expander("Parâmetros"):
            self.m_col1, self.m_col2, self.m_col3 = st.columns(3)
            self.tabela = self.m_col1.selectbox("Tipo de Tabela", ["PF", "PJ", "FCOeBNDES", "FBL"])
            self.dados = self.carregar_dados_tabela(self.tabela)

        self.p_col1, self.p_col2 = st.columns(2)

    def carregar_dados_tabela(self, tabela):
        """Carrega os dados de acordo com o tipo de tabela selecionado."""
        try:
            return pd.read_excel("Data/Base.xlsx", sheet_name=tabela)
        except FileNotFoundError:
            st.error("O arquivo 'Base.xlsx' não foi encontrado.")
            st.stop()

    def carregar_rodape_e_selo(self):
        """Carrega o rodapé e o selo da página."""
        col1, col2, col3 = st.columns([1, 3, 1])
        col2.markdown("<p style='text-align: center; color: #C9D200; font-size: 20px;'></p>", unsafe_allow_html=True)
        col2.markdown("<p style='text-align: center; color: #C9D200; font-size: 20px;'>Desenvolvido pela equipe de BI no departamento de Controladoria!</p>", unsafe_allow_html=True)

    def main(self):
        """Função principal que gerencia a lógica da interface."""
        self.natureza = self.m_col2.selectbox("Natureza", ["Pré-fixada", "Pós-fixada"], index=None, placeholder="Escolha uma natureza")
        self.risco = self.m_col3.selectbox("Risco", ["A", "B", "C", "D"], index=None, placeholder="Escolha a letra de risco")
        
        self.linha = self.m_col1.selectbox("Linha", self.dados["LINHAS DE CRÉDITO"].unique(), index=None, placeholder="Escolha a linha")
        dados_filtrados = self.dados[self.dados["LINHAS DE CRÉDITO"] == self.linha]
        
        self.n_linha = self.m_col2.selectbox("Número da Linha", dados_filtrados["Nº DE LINHA"].unique(), index=None, placeholder="Escolha o número da linha")
        dados_filtrados = dados_filtrados[dados_filtrados["Nº DE LINHA"] == self.n_linha]
        
        self.prazo = self.m_col3.selectbox("Prazo", dados_filtrados["PRAZO"].unique(), index=None, placeholder="Escolha o prazo")
        dados_filtrados = dados_filtrados[dados_filtrados["PRAZO"] == self.prazo]

        if self.campos_preenchidos():
            self.tx_final = self.calcular_taxa_final(dados_filtrados, self.natureza, self.risco)
            self.exibir_taxas(self.tx_final)
        else:
            st.success("Por favor, preencha todos os campos para calcular a taxa!")

        # Gerencia as ações de exportar e enviar e-mail
        self.gerenciar_exportacao_e_envio_email()
        # Carrega o rodapé e o selo da página
        self.carregar_rodape_e_selo()

    def calcular_taxa_final(self, dados, natureza, risco):
        """Calcula a taxa final com base na natureza e no risco."""
        if self.campos_preenchidos():
            match natureza:
                case "Pré-fixada":
                    return self.obter_taxa_por_risco(dados, f"RISCO {risco} - PRÉ")
                case "Pós-fixada":
                    return self.obter_taxa_por_risco(dados, f"RISCO {risco} - PÓS")
    
    def obter_taxa_por_risco(self, dados, nome_coluna):
        """Calcula a taxa com base no risco e retorna o valor arredondado."""
        return round(pd.to_numeric(dados[nome_coluna]).sum() * 100, 2)

    def exibir_taxas(self, tx_final):
        """Exibe as taxas calculadas na interface."""
        if tx_final:
            self.p_col1.metric("Taxa Balcão (a.m)", f"{tx_final}%")
            self.p_col2.metric("Taxa Balcão (a.a)", f"{round(100 * (((1 + (tx_final / 100)) ** 12) - 1), 2)}%")
        else:
            tx_final = 0
            self.p_col1.metric("Taxa Balcão (a.m)", f"{tx_final}%")
            self.p_col2.metric("Taxa Balcão (a.a)", f"{round(100 * (((1 + (tx_final / 100)) ** 12) - 1), 2)}%")

    def gerenciar_exportacao_e_envio_email(self):
        """Gerencia as ações de exportar o PDF e enviar o e-mail."""
         # Criação de colunas para centralizar os botões
        col1, col2, col3, col4 = st.columns([1, 1.25, 1, 1])
        simul_salva = False
        
        with col2:
            exportar = st.button('Salvar Simulação', on_click=self.gravar_valores)
            
            if exportar:
                if self.campos_preenchidos():
                    simul_salva = True
                    caminhpo_pdf = self.gerar_exportacao_pdf()
                    with open(caminhpo_pdf, "rb") as file:
                                st.download_button('Baixar Arquivo', data=file, file_name=caminhpo_pdf)
                    # Botão para alternar para a tela de Taxa Diferenciada
                    
        with col3:
            enviar_email = st.button('Enviar para Análise')
            
            if enviar_email:
                self.enviar_simulacao_email()
                    
    def gerar_exportacao_pdf(self):
        """Exporta a simulação para PDF."""
        if self.campos_preenchidos():
            nome_ger = st.session_state['nome'] 
            numero_pa = st.session_state['numero_pa']
            nome_pa = st.session_state['nome_pa']
            email = st.session_state['email']
            
            with st.spinner("Gerando PDF..."):
                try:
                    caminho_pdf = self.exportar_pdf(tx_final=self.tx_final, tabela=self.tabela, natureza=self.natureza, 
                                                    risco=self.risco, linha=self.linha, n_linha=self.n_linha, prazo=self.prazo, 
                                                    nome_cli=self.nome, nome_ger=nome_ger, num_pa=numero_pa, nome_pa=nome_pa, 
                                                    email=email)
                    st.success("PDF gerado com sucesso!")
                    
                    return caminho_pdf
                except Exception as e:
                    st.error(f"Ocorreu um erro ao gerar o PDF: {e}")

    @staticmethod
    def exportar_pdf(tx_final, tabela, natureza, risco, linha, n_linha, prazo, nome_cli, nome_ger, nome_pa, num_pa, email):
        pdf = Criar_PDF()
        return pdf.gerar_pdf(tx_final=tx_final, tabela=tabela, natureza=natureza, risco=risco, 
                             linha=linha, n_linha=n_linha, prazo=prazo, nome_cli=nome_cli, 
                             nome_ger=nome_ger, nome_pa=nome_pa, num_pa=num_pa, email=email )

    def enviar_simulacao_email(self):
        """Envia a simulação por e-mail."""
        if self.campos_preenchidos():
            with st.spinner("Enviando e-mail..."):
                try:
                    self.enviar_email()
                    st.success("E-mail enviado com sucesso!")
                except Exception as e:
                    st.error(f"Ocorreu um erro ao enviar o e-mail: {e}")

    def enviar_email(self):
        email = Sender_email(nome_cooperado=self.nome, linha=self.linha, taxa=self.tx_final)
        return email.enviar()

    def campos_preenchidos(self):
        """Verifica se todos os campos necessários estão preenchidos."""
        return all([self.nome, self.tabela, self.natureza, self.risco, self.linha, self.n_linha, self.prazo])

if __name__ == "__main__":
    Simulador()
