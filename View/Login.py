import streamlit as st
import duckdb
import hashlib
import pandas as pd

class Login():
    def __init__(self):
        # Conectando ao DuckDB (ou criando o banco de dados em um arquivo)
        self.conn = duckdb.connect('Data/bd_prec.db')

        # Criando a tabela de usuários, caso ainda não exista, com as colunas adicionais
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                email VARCHAR PRIMARY KEY,
                senha_hash VARCHAR,
                nome VARCHAR,
                numero_pa VARCHAR,
                nome_pa VARCHAR,
                perfil VARCHAR
                
            )
        ''')
        
        self.email=""

    def carregar_logo_e_titulo(self):
        """Carrega o logo e o título da página."""
        col1, col2 = st.columns([0.5, 2])
        col1.image('Images/Logo.png', width=100, use_column_width="always")
        col2.markdown("<h1 style='text-align: center; color: #C9D200;'>Login em Taxas de Crédito</h1>", unsafe_allow_html=True)

    def hash_senha(self, senha):
        """Retorna o hash SHA-256 da senha fornecida."""
        return hashlib.sha256(senha.encode()).hexdigest()

    def registrar_usuario(self, email, senha, nome, numero_pa, nome_pa, perfil):
        """Registra um novo usuário com o email, senha criptografada e informações adicionais."""
        senha_hash = self.hash_senha(senha)
        try:
            self.conn.execute('INSERT INTO usuarios (email, senha_hash, nome, numero_pa, nome_pa, perfil) VALUES (?, ?, ?, ?, ?, ?)', 
                              (email, senha_hash, nome, numero_pa, nome_pa, perfil))
            st.success(f"Usuário {email} registrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao registrar usuário: {str(e)}")
        # Atualiza a lista de usuários após o registro
        self.mostrar_usuarios()

    def verificar_login(self, email, senha):
        """Verifica se o login é válido comparando o hash da senha."""
        senha_hash = self.hash_senha(senha)
        result = self.conn.execute('SELECT senha_hash FROM usuarios WHERE email = ?', (email,)).fetchone()
        
        if result and result[0] == senha_hash:
            return True
        return False
    
    def logar(self):
        if st.session_state['tela_ativa'] == 'login':
            # Tela de Login
            self.carregar_logo_e_titulo()

            # Campo para E-mail
            self.email = st.text_input("Email")
            st.session_state['email'] = self.email
            # Campo para Senha (oculta os caracteres)
            senha = st.text_input("Senha", type="password")

            # Botão de Login
            if st.button("Login"):
                if self.verificar_login(self.email, senha):
                    st.session_state['logged_in'] = True
                    return True
                else:
                    st.error("Email ou senha incorretos. Tente novamente.")

    def registrar_novo_usuario(self):
        with st.expander("Registrar Usuário"):
            """Tela para registrar novos usuários."""
            
            # Campos de E-mail, Senha, Nome, Número PA e Nome PA para registro
            email = st.text_input("Novo Email")
            senha = st.text_input("Nova Senha", type="password")
            nome = st.text_input("Nome")
            numero_pa = st.text_input("Número PA")
            nome_pa = st.text_input("Nome PA")
            perfil = st.text_input("Perfil")
            
            # Botão para registrar
            if st.button("Registrar"):
                if email and senha and nome and numero_pa and nome_pa and perfil:
                    self.registrar_usuario(email, senha, nome, numero_pa, nome_pa, perfil)
                else:
                    st.error("Por favor, preencha todos os campos.")
    
    # Função para apagar usuário
    def apagar_usuario(self):
        with st.expander("Apagar Usuário"):
            """Interface para apagar um usuário do banco de dados."""
            # Campo para o email do usuário que será apagado
            email = st.text_input("Email do Usuário para apagar")

            # Botão para apagar o usuário
            if st.button("Apagar Usuário"):
                if email:
                    try:
                        self.conn.execute('DELETE FROM usuarios WHERE email = ?', (email,))
                        st.success(f"Usuário {email} apagado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao apagar usuário: {str(e)}")
                    # Atualiza a lista de usuários após a exclusão
                    self.mostrar_usuarios()
                else:
                    st.error("Por favor, preencha o campo de email.")

    # Função para editar usuário
    def editar_usuario(self):
        with st.expander("Editar Usuário"):
            """Interface para editar email e/ou senha de um usuário."""
            # Campo para o email antigo do usuário
            email_antigo = st.text_input("Email do Usuário para editar")

            # Campos para o novo email, nova senha, Nome, Número PA e Nome PA
            email_novo = st.text_input("Novo Email (deixe em branco se não quiser mudar)")
            senha_nova = st.text_input("Nova Senha (deixe em branco se não quiser mudar)", type="password")
            nome = st.text_input("Nome (deixe em branco se não quiser mudar)")
            numero_pa = st.text_input("Número PA (deixe em branco se não quiser mudar)")
            nome_pa = st.text_input("Nome PA (deixe em branco se não quiser mudar)")
            perfil = st.text_input("Perfil (deixe em branco se não quiser mudar)")

            # Botão para editar o usuário
            if st.button("Editar Usuário"):
                if email_antigo:
                    try:
                        if email_novo:
                            self.conn.execute('UPDATE usuarios SET email = ? WHERE email = ?', (email_novo, email_antigo))
                        if senha_nova:
                            senha_hash_nova = self.hash_senha(senha_nova)
                            self.conn.execute('UPDATE usuarios SET senha_hash = ? WHERE email = ?', (senha_hash_nova, email_novo or email_antigo))
                        if nome:
                            self.conn.execute('UPDATE usuarios SET nome = ? WHERE email = ?', (nome, email_novo or email_antigo))
                        if numero_pa:
                            self.conn.execute('UPDATE usuarios SET numero_pa = ? WHERE email = ?', (numero_pa, email_novo or email_antigo))
                        if nome_pa:
                            self.conn.execute('UPDATE usuarios SET nome_pa = ? WHERE email = ?', (nome_pa, email_novo or email_antigo))
                        if perfil:
                            self.conn.execute('UPDATE usuarios SET perfil = ? WHERE email = ?', (perfil, email_novo or email_antigo))
                        st.success(f"Usuário {email_antigo} atualizado com sucesso!")
                        # Atualiza a lista de usuários após a edição
                        self.mostrar_usuarios()
                    except Exception as e:
                        st.error(f"Erro ao atualizar usuário: {str(e)}")
                else:
                    st.error("Por favor, preencha o campo de email.")
              
    # Função para mostrar todos os usuários
    def mostrar_usuarios(self):
        with st.container(border=True):
            """Interface para listar todos os usuários do banco de dados em uma tabela formatada."""
            st.markdown("<h2 style='text-align: center; color: #C9D200;'>Usuários Registrados</h2>", unsafe_allow_html=True)
            
            try:
                # Recupera todos os emails, nomes, números PA e nomes PA da tabela de usuários
                usuarios = self.conn.execute('SELECT email, perfil FROM usuarios').fetchall()
                
                if usuarios:
                    # Converte a lista de tuplas em um DataFrame do Pandas para exibição
                    df = pd.DataFrame(usuarios, columns=['Email', 'Perfil'])

                    # Exibe a tabela com os usuários usando dataframe
                    st.dataframe(df.style.hide(axis='index'), use_container_width=True)
                else:
                    st.warning("Nenhum usuário encontrado.")
            except Exception as e:
                st.error(f"Erro ao recuperar usuários: {str(e)}")
    
    def obter_dados_usuarios(self):
        try:
            # Recupera todos os emails, nomes, números PA e nomes PA da tabela de usuários
            usuarios = self.conn.execute('SELECT nome, numero_pa, nome_pa, perfil FROM usuarios WHERE email = ?', (st.session_state['email'],)).fetchone()
            
            if usuarios:
                st.session_state['nome'] = usuarios[0]
                st.session_state['numero_pa'] = usuarios[1]
                st.session_state['nome_pa'] = usuarios[2]
                st.session_state['perfil'] = usuarios[3]
            else:
                st.warning("Nenhum usuário encontrado.")
                
        except Exception as e:
            st.error(f"Erro ao recuperar usuários: {str(e)}")

"""
if __name__ == "__main__":
    Login()
    Login().registrar_usuario(email="matheusVC", senha="123", nome="Matheus Vicente", numero_pa="99", nome_pa="UAD", perfil="user") 
    
"""

