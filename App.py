import streamlit as st
import pandas as pd
from Views.Tx_Simulador import Simulador
from Views.Tx_Diferenciada import Taxa_Diferenciada
from Views.Tx_Precificador import Precificador
from Views.Login import Login
from Views.Cons_Simulador import Consulta_Simulacao
from Controllers.Handler_Export import Lidar_Dir
from Controllers.Query_Simulador import Simulacao

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
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background-color: #161a1a !important;
        color: #ffffff !important;
    }
    h1, h2, h3 {
        color: #7DB61C !important;
    }
    
    [data-testid="stImage"] a {
        display: none;
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
    </style>
    """,
    unsafe_allow_html=True
)

class APP_GUI(Login, Simulacao):
    def __init__(self): 
        Login.__init__(self)
        Simulacao.__init__(self)
        self.consulta = Consulta_Simulacao()
        
        self.simulador = None
        self.inicializar_sessao()
        
    def inicializar_sessao(self):
        """Gerencia o estado da sessão de forma persistente"""
        
        if 'reloaded' not in st.session_state:
            st.session_state['reloaded'] = False
            
        if not st.session_state['reloaded']:
            if 'logged_in' not in st.session_state:
                st.session_state['logged_in'] = False
        
            if 'tela_ativa' not in st.session_state:
                st.session_state['tela_ativa'] = 'login'  
                
            st.session_state['reloaded'] = True
        
        if st.session_state['logged_in']:
            self.obter_dados_usuarios()
            Lidar_Dir(st.session_state['email'])
            self.navegar_paginas()
        else:
            self.mostrar_login()
    
    def mostrar_login(self):
        """Exibe a tela de login e redireciona após o login"""
        resultado_login = self.logar()
        if resultado_login:
            st.session_state['logged_in'] = True
            st.session_state['tela_ativa'] = 'simulador'
            st.rerun()  # Garante que a navegação ocorra sem travamentos
    
    def navegar_paginas(self):
        """Controla a navegação entre as páginas"""
        with st.sidebar:        
            col1, col2, col3 = st.columns([0.25,1,0.25])
            with col2:
                st.image('Images/Logo_side.png', width=80, use_column_width="always")
                st.write("")
                st.write(f"**Nome:** {st.session_state.get('nome', 'Nome não definido')}")
                st.write(f"**E-mail:** {st.session_state.get('email', 'E-mail não definido')}")
                st.write(f"**Agência:** {st.session_state.get('nome_pa', 'Agência não definida')} | Nº: {st.session_state.get('numero_pa', '999')}")

                pag = st.selectbox("Escolha a página", ["Simulação de Taxa", "Solicitar Desconto de Taxa", "Consultar Simulações", "Mesa de Precificação", "Painel de Controle"])

        if pag == "Simulação de Taxa":
            self.mostrar_simulador()
        elif pag == "Solicitar Desconto de Taxa":
            self.mostrar_tx_diferenciada()
        elif pag == "Mesa de Precificação":
            self.mostrar_precificador()
        elif pag == "Consultar Simulações":
            self.consulta.mostrar_reg_simul()
        elif pag == "Painel de Controle":
            self.mostrar_painel_controle()
       
            
        with col2:
            if st.button("Sair"):
                Lidar_Dir(st.session_state['email']).limpar_dir()
                st.session_state.clear()
                st.rerun()
                
            st.write("**Desenvolvido pela Equipe de Inteligência Operacional**")
            
    def mostrar_simulador(self):
        """Exibe a página de simulação de taxa"""
        if not self.simulador:
            self.simulador = Simulador()
        self.simulador.mostrar_simulador()
        
    def mostrar_todas_simulacao(self):
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #C9D200;'>Simulações Registradas</h2>", unsafe_allow_html=True)
            
            try:
                # Recupera todos os emails, nomes, números PA e nomes PA da tabela de usuários
                simulacoes = self.ler_simulacao()
                
                if simulacoes:
                    # Converte a lista de tuplas em um DataFrame do Pandas para exibição
                    df = pd.DataFrame(simulacoes, columns=['Nº SIM', 'Taxa', 'Tabela', 'Natureza', 
                                                           'Risco', 'Linha', 'Nº Linha', 'Prazo', 'Nome Cliente', 
                                                           'Nome Gerente', 'Nome PA', 'Nº PA', 'Email', "Defesa"])

                    # Exibe a tabela com os usuários usando dataframe
                    st.dataframe(df.style.hide(axis='index'), use_container_width=True)
                else:
                    st.warning("Nenhuma simulação cadastrada.")
            except Exception as e:
                st.error(f"Erro ao recuperar simulações: {str(e)}")
        
    def mostrar_tx_diferenciada(self):
        """Exibe a página de solicitação de desconto de taxa"""
        taxa = st.session_state.get('taxa')
        tabela = st.session_state.get('tabela')
        natureza = st.session_state.get('natureza')
        risco = st.session_state.get('risco')
        linha = st.session_state.get('linha')
        n_linha = st.session_state.get('n_linha')
        prazo = st.session_state.get('prazo')
        nome = st.session_state.get('nome')
        
        if all([nome, tabela, natureza, risco, linha, n_linha, prazo]):
            tx_dif = Taxa_Diferenciada(tx=taxa, tabela=tabela, natureza=natureza, risco=risco, linha=linha, n_linha=n_linha, prazo=prazo, nome_cli=nome)
            tx_dif.mostrar_pagina()
        else:
            st.error("Necessário simular uma taxa antes de solicitar o desconto!")
        
    def mostrar_precificador(self):
        """Exibe a página de mesa de precificação"""
        precificador = Precificador()
        precificador.mostrar_precificador()

    def mostrar_painel_controle(self):
        """Exibe o painel de controle, apenas para admins"""
        if st.session_state.get('perfil') == 'admin':
            self.mostrar_todas_simulacao()
            self.mostrar_usuarios()
            self.registrar_novo_usuario()
            self.editar_usuario()
            self.apagar_usuario()
        else:
            st.warning("Você não possui permissão para acessar esta página.")

if __name__ == "__main__":
    APP_GUI()
