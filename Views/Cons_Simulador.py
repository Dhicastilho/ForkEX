#Importando as bibliotecas que serão utilizadas
import streamlit as st
import pandas as pd
from Controllers.Export_PDF import Criar_PDF
from Controllers.Query_Simulador import Simulacao

class Consulta_Simulacao(Simulacao):
    def __init__(self):
        Simulacao.__init__(self)
        
    def mostrar_cos_sim(self):
        self.exibir_cabecalho()
        self.mostrar_reg_simul()
        
    def exibir_cabecalho(self):
        #Título da Página e Logo
        col1, col2, col3 = st.columns(3)
        col2.image('Images/Logo.png', width=100, use_column_width="always")

        col1,= st.columns(1)
        col1.markdown("<h1 style='text-align: center; color: #C9D200;'>Consultar as Simulações</h1>", unsafe_allow_html=True)
        col1.markdown("<h1></h1>", unsafe_allow_html=True)
        
        #Taxas
        with st.container(border=True):
            self.p_col1, self.p_col2, self.p_col3, self.p_col4, self.p_col5, self.p_col6 = st.columns(6)

    def mostrar_reg_simul(self):
        email = st.session_state['email']
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #C9D200;'>Simulações Registradas</h2>", unsafe_allow_html=True)
            
            try:
                # Recupera todos os emails, nomes, números PA e nomes PA da tabela de usuários
                simulacoes = self.ler_simulacao_PorEmail(email)
                print(simulacoes)
                
                if simulacoes:
                    # Converte a lista de tuplas em um DataFrame do Pandas para exibição
                    df = pd.DataFrame(simulacoes, columns=['Nº SIM', 'Taxa', 'Tabela', 'Natureza', 
                                                           'Risco', 'Linha', 'Nº Linha', 'Prazo', 'Nome Cliente', 
                                                           'Nome Gerente', 'Nome PA', 'Nº PA', 'Email', 'Defesa'])

                    # Exibe a tabela com os usuários usando dataframe
                    st.dataframe(df.style.hide(axis='index'), use_container_width=True)
                else:
                    st.warning("Nenhuma simulação cadastrada.")
            except Exception as e:
                st.error(f"Erro ao recuperar simulações: {str(e)}") 
        
        simul_select = st.text_input("Número da Simulação:", placeholder="Insira aqui o número da simulação que deseja exportar:")
        if st.button("Filtrar"):
            dados_export = df[df['Nº SIM'].astype(str) == simul_select]
            dados_lista = dados_export.values.tolist()[0]
            
            try:
                caminho_pdf = self.exportar_pdf(
                    tx_final=round(dados_lista[1],2),
                    tabela=dados_lista[2],
                    natureza=dados_lista[3],
                    risco=dados_lista[4],
                    linha=dados_lista[5],
                    n_linha=dados_lista[6],
                    prazo=dados_lista[7],
                    nome_cli=dados_lista[8],
                    nome_ger=dados_lista[9],
                    nome_pa=dados_lista[10],
                    num_pa=dados_lista[11],
                    email=dados_lista[12],
                    defesa = dados_lista[13]
                )

                with open(caminho_pdf, "rb") as file:
                    st.download_button('Baixar Arquivo (.pdf)', data=file, file_name=caminho_pdf)

            except Exception as e:
                st.error(f"Erro ao exportar PDF: {str(e)}")
                
    
    @staticmethod
    def exportar_pdf(tx_final, tabela, natureza, risco, linha, n_linha, prazo, nome_cli, nome_ger, nome_pa, num_pa, email, defesa):
        pdf = Criar_PDF()
        return pdf.gerar_pdf(tx_final=tx_final, tabela=tabela, natureza=natureza, risco=risco, 
                             linha=linha, n_linha=n_linha, prazo=prazo, nome_cli=nome_cli, 
                             nome_ger=nome_ger, nome_pa=nome_pa, num_pa=num_pa, email=email, defesa=defesa )
   
            
if __name__ == "__main__": 
    Consulta_Simulacao()