import streamlit as st
import win32com.client as win32
import pythoncom
from View.Tx_Simulador import Simulador
from View.Tx_Diferenciada import Taxa_Diferenciada
from View.Tx_Precificador import Precificador
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
    /* Forçar o fundo escuro para toda a aplicação */
    .stApp {
        background-color: #161a1a !important;
        color: #ffffff !important;
    }

    /* Sidebar com fundo verde médio */
    .css-1d391kg {
        background-color: #1c1c1c !important;
        color: #ffffff !important;
    }

    /* Cabeçalhos e títulos com cor turquesa */
    h1, h2, h3 {
        color: #7DB61C !important;
    }
    
     /* Parágrafo como branco*/
    p {
        color: #ffffff !important;
    }

    /* Botões com fundo verde escuro */
    .stButton>button {
        background-color: #003641 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }

    /* Selectbox e dropdown com fundo verde escuro e texto branco */
    .stSelectbox>div>div, .stMultiSelect>div>div, .stDropdown>div>div {
        background-color: #003641 !important;
        color: white !important;
    }

    /* Inputs de texto com borda branca e fundo escuro */
    .stTextInput>div>input {
        background-color: #262729 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
    }

    /* Remover qualquer destaque de foco vermelho */
    input:focus, textarea:focus, select:focus, .stSelectbox>div>div:focus, .stMultiSelect>div>div:focus, .stDropdown>div>div:focus {
        outline: #ffffff !important;
        box-shadow: #ffffff !important;
        border-color: #ffffff !important;
    }

    /* Customização das cores do texto no sidebar */
    .css-16huue1 {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the structure of the app GUI
class APP_GUI:
    def __init__(self): 
        # Initialize the COM interface and Outlook
        pythoncom.CoInitialize()
        self.outlook = win32.Dispatch('outlook.application')
        
        # Initialize the session
        self.inicializar_sessao()
        
        # Navigate between the pages
        self.navegar_paginas()
        
    def inicializar_sessao(self):
        """Initializes the session and clears the Export folder on first startup."""
        if 'initialized' not in st.session_state:
            Tratar_Arquivos()  # Function to handle files on first startup
            st.session_state['initialized'] = True

    def navegar_paginas(self):
        """Navigates between the available pages in the app."""
        # Clear the sidebar to not show files
        st.sidebar.empty()  # Removes previous content from the sidebar

        # Sidebar menu to choose the page
        pag = st.sidebar.selectbox("Escolha a página", ["Simulação de Taxa", "Solicitação de Taxa Diferenciada", "Mesa de Precificação"])

        # Instantiate the rate simulation page
        simulador = Simulador()
        precificador = Precificador()
        
        tx_final = simulador.obter_tx_final()
        
        try:
            page_tx_diferenciada = Taxa_Diferenciada(tx_final)
        
        except:
            st.warning("É necessário simular uma taxa primeiramente")
            
        if pag == "Simulação de Taxa":
            # Renderiza a página
            simulador.mostrar_simulador()
            
        elif pag == "Solicitação de Taxa Diferenciada":
            # Renderiza a página
            page_tx_diferenciada.mostrar_pagina()
            
        elif pag == "Mesa de Precificação":
            # Renderiza a página
            precificador.mostrar_precificador()
        
        else:
            st.warning("Escolha uma página")
            
if __name__ == "__main__":
    APP_GUI()
