import streamlit as st

class Login():
    def __init__(self):
        # Simulando um banco de dados simples de usuários (pode ser substituído por uma autenticação real)
        self.usuarios = {
            "matheus": "123"
        }

    def carregar_logo_e_titulo(self):
        """Carrega o logo e o título da página."""
        col1, col2 = st.columns([0.5, 2])
        col1.image('Images/Logo.png', width=100, use_column_width="always")
        col2.markdown("<h1 style='text-align: center; color: #C9D200;'>Login em Taxas de Crédito</h1>", unsafe_allow_html=True)

    def logar(self):
        
        if st.session_state['tela_ativa'] == 'login':
            # Tela de Login
            self.carregar_logo_e_titulo()

            # Campo para E-mail
            email = st.text_input("Email")

            # Campo para Senha (oculta os caracteres)
            senha = st.text_input("Senha", type="password")

            # Botão de Login
            if st.button("Login"):
                if email in self.usuarios and self.usuarios[email] == senha:
                    st.success("Login realizado com sucesso!")
                    return True
                else:
                    st.error("Email ou senha incorretos. Tente novamente.")
                    return False