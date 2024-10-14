import streamlit as st

class Taxa_Diferenciada():
    def __init__(self, tx):
        # Recebe a taxa simulada como argumento e define o valor máximo da taxa diferenciada
        self.tx_final = tx
        self.tx_minima = round(tx * 0.8, 2)
        
    def mostrar_pagina(self):
        """Exibe os componentes da página de solicitação de taxa diferenciada."""
        self.carregar_logo_e_titulo()
        self.exibir_taxas()
        self.iniciar_solicitacao()
        self.carregar_rodape()

    def carregar_logo_e_titulo(self):
        """Carrega o logo e o título da página."""
        col1, col2 = st.columns([0.5, 2])
        col1.image('Images/Logo.png', width=100, use_column_width="always")
        col2.markdown("<h1 style='text-align: center; color: #C9D200;'>Solicitar Taxa Diferenciada</h1>", unsafe_allow_html=True)

    def exibir_taxas(self):
        """Exibe a taxa precificada e a taxa mínima permitida."""
        st.metric("Taxa Precificada (a.m)", f"{self.tx_final}%")
        st.metric("Taxa Mínima Permitida (a.m)", f"{self.tx_minima}%")

    def iniciar_solicitacao(self):
        """Inicia o input para o usuário solicitar a taxa diferenciada."""
        taxa_solicitada = st.number_input(
            "Insira a taxa diferenciada desejada (no máximo 20% menor que a taxa simulada):",
            min_value=float(self.tx_minima),
            max_value=float(self.tx_final),  
            value=float(self.tx_final),     
            step=0.1                        
        )

        if st.button("Solicitar Taxa Diferenciada"):
            self.solicitar_taxa(taxa_solicitada)

    def solicitar_taxa(self, taxa_solicitada):
        """Lógica para processar a solicitação da taxa diferenciada."""
        st.success(f"Solicitação enviada com sucesso! Taxa solicitada: {taxa_solicitada}%")
        # Aqui você pode adicionar a lógica para enviar um e-mail ou salvar a solicitação no banco de dados

    def carregar_rodape(self):
        """Carrega o rodapé da página."""
        col1, col2, col3= st.columns([1, 3, 1])
        col2.markdown("<p style='text-align: center; color: #C9D200; font-size: 20px;'></p>", unsafe_allow_html=True)
        col2.markdown("<p style='text-align: center; color: #C9D200; font-size: 20px;'>Desenvolvido pela equipe de BI no departamento de Controladoria!</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    Taxa_Diferenciada()