import streamlit as st
import pandas as pd
from Controllers.Export_PDF import Criar_PDF
from Controllers.Sender import Sender_email
from Controllers.Query_Simulador import Simulacao
from Controllers.Calculator import Calcular_CET

class Simulador(Simulacao):
    def __init__(self):
        Simulacao.__init__(self)
        
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
        self.defesa = ""
        self.saldo_dev = 0.0
        self.prazo_op = 0.0
        self.parcela = 0.0
        self.CET = 0.0

        # Inicializa a tela ativa no estado da sessão (tela padrão: Simulação)
        if 'tela_ativa' not in st.session_state:
            st.session_state['tela_ativa'] = 'simulador'

    def mostrar_simulador(self):
        self.carregar_logo_e_titulo()
        self.inicializar_componentes()
        self.main()
            
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

        self.p_col1, self.p_col2, self.p_col3, self.p_col4, self.p_col5, self.p_col6 = st.columns(6)

    def carregar_dados_tabela(self, tabela):
        """Carrega os dados de acordo com o tipo de tabela selecionado."""
        try:
            return pd.read_excel("Data/Base.xlsx", sheet_name=tabela)
        except FileNotFoundError:
            st.error("O arquivo 'Base.xlsx' não foi encontrado.")
            st.stop()

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
        
        self.saldo_dev = self.m_col1.text_input("Valor da Operação", placeholder="Insira o valor da operaçãos em R$")
        self.prazo_op = self.m_col2.text_input("Prazo da Operação", placeholder="Insira o prazo da operaçãos em meses")
        self.tabela_op = self.m_col3.selectbox("Tabela da Operação:",["SAC", "PRICE"], index=None, placeholder="Escolha uma tabela para a operação")
        
        calc = Calcular_CET()

        try:
            # Calcula o IOF
            iof = calc.calcular_iof(float(self.saldo_dev), int(self.prazo_op))
            
            # Verifica o tipo de tabela selecionado (SAC ou Price)
            if self.tabela_op == "SAC":
                self.parcela = calc.calcular_sac(float(self.saldo_dev), float(self.tx_final), int(self.prazo_op), iof)
                
                print(self.parcela)  # Exibe todas as parcelas
                
                self.CET = calc.calcular_CET(float(self.tx_final), int(self.prazo_op), iof)
            elif self.tabela_op == "PRICE":
                self.parcela = calc.calcular_price(float(self.saldo_dev), float(self.tx_final), int(self.prazo_op), iof)
                print(self.parcela)  # Exibe a parcela fixa (Price)
                self.CET = calc.calcular_CET(float(self.tx_final), int(self.prazo_op), iof)

            # Exibe o resultado do CET
            st.write(f"CET calculado: {self.CET:.2f}")
            
        except Exception as e:
            print("")
        
        self.defesa = st.text_area("Defesa da Proposta", height=200)

        if self.campos_preenchidos():
            self.tx_final = self.calcular_taxa_final(dados_filtrados, self.natureza, self.risco)
            self.exibir_taxas(tx_final=self.tx_final, CET=self.CET, parcela=self.parcela, saldo_dev=self.saldo_dev, prazo_op=self.prazo_op)

        # Gerencia as ações de exportar e enviar e-mail
        self.gerenciar_exportacao_e_envio_email()
    	
     
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

    def exibir_taxas(self, tx_final, CET, parcela, saldo_dev, prazo_op):
        """Exibe as taxas calculadas na interface."""
        if tx_final:
            self.p_col1.metric("Taxa Balcão (a.m)", f"{tx_final} %")
            self.p_col2.metric("Taxa Balcão (a.a)", f"{round(100 * (((1 + (tx_final / 100)) ** 12) - 1), 2)} %")
            self.p_col3.metric("CET (a.m)", f"{CET} %")
            self.p_col4.metric("Saldo Devedor", f"{float(saldo_dev):,.2f} R$")
            self.p_col5.metric("Parcela", f"{float(parcela):,.2f} R$")
            self.p_col6.metric("Prazo", f"{prazo_op} meses")
            
        else:
            tx_final = 0
            self.p_col1.metric("Taxa Balcão (a.m)", f"{tx_final}%")
            self.p_col2.metric("Taxa Balcão (a.a)", f"{round(100 * (((1 + (tx_final / 100)) ** 12) - 1), 2)}%")
            self.p_col3.metric("CET (a.m)", f"{round(100*CET,2)} %")
            self.p_col4.metric("Saldo Devedor", f"{float(saldo_dev):,.2f} R$")
            self.p_col5.metric("Parcela", f"{float(parcela):,.2f} R$")
            self.p_col6.metric("Prazo", f"{prazo_op} meses")

    def gravar_valores(self):
        # Salvar valores na sessão do Streamlit
        st.session_state['taxa'] = self.tx_final
        st.session_state['tabela'] = self.tabela
        st.session_state['natureza'] = self.natureza
        st.session_state['risco'] = self.risco
        st.session_state['linha'] = self.linha
        st.session_state['n_linha'] = self.n_linha
        st.session_state['prazo'] = self.prazo
        st.session_state['nome_cli'] = self.nome
        st.session_state["defesa"] = self.defesa

    def gravar_simulacao_BD(self):
        """Grava a simulação no BD."""
        
        nome_ger = st.session_state['nome'] 
        numero_pa = st.session_state['numero_pa']
        nome_pa = st.session_state['nome_pa']
        email = st.session_state['email']
        taxa = st.session_state['taxa'] 
        tabela = st.session_state['tabela']
        natureza =st.session_state['natureza']
        risco = st.session_state['risco']
        linha = st.session_state['linha']
        n_linuha = st.session_state['n_linha']
        prazo = st.session_state['prazo']
        nome_cli = st.session_state['nome_cli'] 
        defesa = st.session_state["defesa"]
        
        self.inserir_simulacao(nome_cli=nome_cli, nome_ger=nome_ger, nome_pa=nome_pa, num_pa=numero_pa, email=email, tx_final=taxa, tabela=tabela, natureza=natureza, risco=risco, linha=linha, n_linha=n_linuha, prazo=prazo, defesa=defesa)

    def gerenciar_exportacao_e_envio_email(self):
        """Gerencia as ações de exportar o PDF e enviar o e-mail."""
         # Criação de colunas para centralizar os botões
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        simul_salva = False
        
        with col3:
            exportar = st.button('Concluir Simulação', on_click=self.gravar_valores)
        
        m_col1, m_col2, m_col3, m_col4, m_col5, m_col6, m_cool7 = st.columns(7)
        if exportar:
            if self.campos_preenchidos():
                
                simul_salva = True
                caminhpo_pdf = self.gerar_exportacao_pdf()
                with open(caminhpo_pdf, "rb") as file:
                    with m_col4:
                        st.download_button('Baixar Arquivo (.pdf)', data=file, file_name=caminhpo_pdf)
                # Botão para alternar para a tela de Taxa Diferenciada
                    
        with col4:
            enviar_email = st.button('Enviar para Análise')
            
            if enviar_email:
                try:
                    self.gravar_simulacao_BD()
                    self.enviar_simulacao_email()
                except:
                    st.error("É necessário concluir a simulação antes de enviar para análise!")        
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
                                                    email=email, defesa=self.defesa)
                    st.success("PDF gerado com sucesso!")
                    
                    return caminho_pdf
                except Exception as e:
                    st.error(f"Ocorreu um erro ao gerar o PDF: {e}")

    @staticmethod
    def exportar_pdf(tx_final, tabela, natureza, risco, linha, n_linha, prazo, nome_cli, nome_ger, nome_pa, num_pa, email, defesa):
        pdf = Criar_PDF()
        return pdf.gerar_pdf(tx_final=tx_final, tabela=tabela, natureza=natureza, risco=risco, 
                             linha=linha, n_linha=n_linha, prazo=prazo, nome_cli=nome_cli, 
                             nome_ger=nome_ger, nome_pa=nome_pa, num_pa=num_pa, email=email, defesa=defesa)

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
        email = Sender_email(nome_cooperado=self.nome, linha=self.linha, taxa=self.tx_final, email=st.session_state['email'])
        return email.enviar()

    def campos_preenchidos(self):
        """Verifica se todos os campos necessários estão preenchidos."""
        return all([self.nome, self.tabela, self.natureza, self.risco, self.linha, self.n_linha, self.prazo, self.defesa])

if __name__ == "__main__":
    Simulador()
