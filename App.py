import streamlit as st
import win32com.client as win32
from View.Tx_Simulador import Simulador
from View.Tx_Diferenciada import Taxa_Diferenciada
from View.Tx_Precificador import Precificador
from View.Login import Login
from Controllers.Moving import Tratar_Arquivos

# Set page configuration with sidebar hidden
st.set_page_config(
    layout="wide", 
    initial_sidebar_state="collapsed",
    page_title="Taxas de Crédito | 3246",
    page_icon="🏦"
)

# Custom CSS to remove red highlights and apply the theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #161a1a !important;
        color: #ffffff !important;
    }
    .css-1d391kg {
        background-color: #1c1c1c !important;
        color: #ffffff !important;
    }
    h1, h2, h3 {
        color: #7DB61C !important;
    }
    p {
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #003641 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }
    .stSelectbox>div>div, .stMultiSelect>div>div, .stDropdown>div>div {
        background-color: #003641 !important;
        color: white !important;
    }
    .stTextInput>div>input {
        background-color: #262729 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
    }
    input:focus, textarea:focus, select:focus {
        outline: #ffffff !important;
        box-shadow: #ffffff !important;
        border-color: #ffffff !important;
    }
    .css-16huue1 {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the structure of the app GUI
class APP_GUI(Login):
    def __init__(self): 
        
        Login.__init__(self) 
        
        # Initialize the session
        self.inicializar_sessao()
        self.simulador = None
    def inicializar_sessao(self):

        if 'initialized' not in st.session_state:
            Tratar_Arquivos()  
            st.session_state['initialized'] = True
        
        
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False
        
        if 'tela_ativa' not in st.session_state:
            st.session_state['tela_ativa'] = 'login'  

        # Verifica se o login foi feito e ajusta a tela ativa
        if st.session_state['logged_in']:
            self.navegar_paginas()
            
        else:
            self.mostrar_login()
    
    def mostrar_login(self):
        """Exibe a tela de login e faz a navegação após o login"""
        if st.session_state['tela_ativa'] == 'login':
            resultado_login = self.logar()
            if resultado_login:
                st.session_state['logged_in'] = True
                st.session_state['tela_ativa'] = 'simulador'
                st.rerun()  # Redireciona para a tela principal após o login

    def navegar_paginas(self):
        """Função para controlar a navegação entre as páginas"""
        # Usar um container para garantir que uma única página seja renderizada
        page_container = st.container()

        with page_container:
            # Limpa a barra lateral
            st.sidebar.empty()

            # Sidebar menu para escolher a página
            pag = st.sidebar.selectbox("Escolha a página", ["Simulação de Taxa", "Solicitar Desconto de Taxa", "Mesa de Precificação"])

            # Carrega as páginas com base na seleção
            if pag == "Simulação de Taxa":
                self.mostrar_simulador()
                st.session_state['tela_ativa'] = 'simulador'
                
            elif pag == "Solicitar Desconto de Taxa":
                self.mostrar_tx_diferenciada()
                st.session_state['tela_ativa'] = 'taxa_diferenciada'
                
            elif pag == "Mesa de Precificação":
                self.mostrar_precificador()
                st.session_state['tela_ativa'] = 'precificador'

    def mostrar_simulador(self):
        """Exibe a página de simulação de taxa"""
        self.simulador = Simulador()
        self.simulador.mostrar_simulador()
    
    def mostrar_tx_diferenciada(self):
        taxa = st.session_state['taxa'] 
        tabela = st.session_state['tabela']
        natureza =st.session_state['natureza']
        risco = st.session_state['risco']
        linha = st.session_state['linha']
        n_linha = st.session_state['n_linha']
        prazo = st.session_state['prazo']
        nome = st.session_state['nome']
        
        if all([nome, tabela, natureza, risco, linha, n_linha, prazo]):
            tx_dif = Taxa_Diferenciada(tx=taxa, tabela=tabela, natureza=natureza, risco=risco, linha=linha, n_linha=n_linha, prazo=prazo, nome=nome)
            tx_dif.mostrar_pagina()
        else:
            st.error("Necessário simular uma taxa antes de solicitar o desconto!")
        
    def mostrar_precificador(self):
        """Exibe a página de mesa de precificação"""
        precificador = Precificador()
        precificador.mostrar_precificador()
            
if __name__ == "__main__":
    APP_GUI()
