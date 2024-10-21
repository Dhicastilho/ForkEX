#Importando as bibliotecas que serão utilizadas
import streamlit as st
import datetime as dt
import pandas as pd

#Função de verificação se é número
def isnumber(value):
    try:
         float(value)
    except ValueError:
         return False
    return True

class Precificador:
    def __init__(self):
        #Dicionário de Nome de PA e seus Números
        self.dict_PA ={
            "Anápolis" : "1", "Castelo Branco" : "2","OCB" : "3", "CASAG" : "4", 
            "POA" : "5", "Caxias do Sul" : "6", "Goianira" : "7", "Cuiabá" : "8",
            "Campo Grande" : "9", "Taguatinga" : "10", "Sede" : "11","Digital" : "97"
        }
        
        self.df_despesas = pd.read_excel("Data/Linhas.xlsx",sheet_name='Despesas')
        self.df_cred = pd.read_excel("Data/Linhas.xlsx",sheet_name='Crédito')
        self.df_CDI = pd.read_excel("Data/Linhas.xlsx",sheet_name='CDI')
        
        self.custo_cred_am = 0
        self.custo_cred_med = 0
        self.tx_inad_am = 0
        self.tx_final = 0
        self.inad_op = ""
        self.spread_op = ""
        self.spread = 0
        self.redutorCC_op = 0
        self.redutorTB_op = 0
        self.tx_final_am = 0
        self.tx_final_aa = 0
        self.cdi_am = 0
        self.cdi_aa = 0
        self.inad_med = 0
        self.spread_CDI = 0
        self.taxa_op = ""
        
        self.p_col1, self.p_col2, self.p_col3, self.p_col4, self.p_col5, self.p_col6 = None, None, None, None, None, None
            
    def mostrar_precificador(self):
        self.exibir_cabecalho()
        self.main()
        
    def exibir_cabecalho(self):
        #Título da Página e Logo
        col1, col2, col3 = st.columns(3)
        col2.image('Images/Logo.png', width=100, use_column_width="always")

        col1,= st.columns(1)
        col1.markdown("<h1 style='text-align: center; color: #C9D200;'>Mesa de Precificação</h1>", unsafe_allow_html=True)
        col1.markdown("<h1></h1>", unsafe_allow_html=True)
        
        #Taxas
        with st.container(border=True):
            self.p_col1, self.p_col2, self.p_col3, self.p_col4, self.p_col5, self.p_col6 = st.columns(6)

    def exibir_taxas(self):
        #Taxas Finais  
        self.p_col1.metric("Taxa Balcão (a.m) " , f"{self.tx_final_am }%", f"{round(self.tx_final_am - self.cdi_am,2)} p.p CDI (a.m)")
        self.p_col2.metric("Taxa Balcão (a.a)" , f"{self.tx_final_aa }%", f"{round(self.tx_final_aa - self.cdi_aa,2)} p.p CDI (a.a)")
        self.p_col3.metric("Inadimplência (a.m)" , f"{self.tx_inad_am}%", f"{round(self.inad_med - self.tx_inad_am,2)}%")
        self.p_col4.metric("Custo do Crédito (a.m)" , f"{self.custo_cred_am}%", f"{round(self.custo_cred_med - self.custo_cred_am,2)}%" )
        self.p_col5.metric("CDI (a.m)" , f"{self.cdi_am}%")
        self.p_col6.metric("Spread em CDI (a.m)" , f"{self.spread_CDI}%", f"{round(self.spread_CDI - self.cdi_am,2)} p.p CDI (a.m)")

    def main(self):
        self.exibir_corpo()
        
        self.custo_cred_med = (-1*self.df_despesas["Despesa ADM"].sum() / self.df_despesas["Saldo Devedor (PA)"].sum())
        self.custo_cred_med = round(self.custo_cred_med*100,2)

        self.inad_med = (self.df_cred["Provisão"].sum() / self.df_cred["Saldo Devedor"].sum()) * 100
        self.inad_med = round(((1+self.inad_med/100)**(1/12)-1)*100,2)
        
        self.cdi = self.df_CDI["CDI"].max() * 100
        
        self.custo_cred = (-1*self.df_despesas["Despesa ADM"].sum()/ self.df_despesas["Saldo Devedor (PA)"].sum())
        self.custo_cred = ((1+ self.custo_cred)**(12)-1)*100

        self.tx_inad = (self.df_cred["Provisão"].sum() / self.df_cred["Saldo Devedor"].sum()) * 100

        self.tx_final = self.tx_final + self.custo_cred
        
        match self.taxa_op:
                case "Pré-fixada":
                    self.tx_final = self.tx_final
                    self.tx_op = 0.00
                    
                case "Pós-fixada":
                    self.tx_final = self.tx_final + self.cdi
                    self.tx_op = self.cdi
        
        match self.inad_op: 
                case "Não":
                    self.tx_final = self.tx_final
                    self.tx_inad = 0.00
                    
                case "Sim":
                    self.tx_final = self.tx_final + self.tx_inad
        
        if isnumber(self.spread_op) == True and self.spread_op !=0:
                self.spread = float(self.spread_op)
                self.spread_op = self.cdi * float(self.spread_op)/100
                self.tx_final = self.tx_final + self.spread_op
                
        else:
            self.tx_final = self.tx_final
            self.spread_op = 0.00
        
        self.cdi_am = round(((1+(self.cdi/100))**(1/12)-1)*100,2)
        self.spread_CDI = round((self.spread/100)*self.cdi_am,2)
        
        if isnumber(self.redutorCC_op) == True and self.redutorCC_op !=0:
            self.custo_cred = self.custo_cred - (self.custo_cred * (float(self.redutorCC_op)/100))
            self.tx_final = self.tx_inad + self.tx_op + self.custo_cred + self.spread_op
                
        else:
            self.tx_final = self.tx_final
            
        if isnumber(self.redutorTB_op) == True and self.redutorTB_op !=0:
            self.tx_final = self.tx_final - (self.tx_final * (float(self.redutorTB_op)/100))
                
        else:
            self.tx_final = self.tx_final
        
        self.custo_cred_am = round(((1+self.custo_cred/100)**(1/12)-1)*100,2)
        self.tx_inad_am = round(((1+self.tx_inad/100)**(1/12)-1)*100,2)
        self.tx_final_am = round((((1 + self.tx_final/100)**(1/12)-1)*100),2)
        self.tx_final_aa = round(self.tx_final, 2)
        self.cdi_am = round(((1+self.cdi/100)**(1/12)-1)*100,2)
        self.cdi_aa = self.cdi
        
        self.exibir_taxas()
        
    def exibir_corpo(self):
        
        with st.expander("Parâmetros"):
            
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            
            col1, col2, col3 = st.columns([3,4,6])

            PA = col1.selectbox("PA", ["Anápolis", "Castelo Branco", "OCB", "CASAG", "POA", "Caxias do Sul", 
                                    "Goianira", "Cuiabá", "Campo Grande", "Taguatinga", "Sede","Digital"])
            
            Num_PA = float(self.dict_PA[PA])

            self.df_cred = self.df_cred[self.df_cred["Número PA"] ==  Num_PA]
            self.df_despesas = self.df_despesas[self.df_despesas["Número PA"] ==  Num_PA]

            pessoa = m_col1.selectbox("Tipo de Pessoa", self.df_cred["Tipo Pessoa"].unique())
            self.df_cred = self.df_cred[self.df_cred["Tipo Pessoa"] == pessoa]  

            risco = m_col2.selectbox("Risco", ["AA", "A", "B", "C", "D", "E", "F", "G", "H"], index=None, 
                                    placeholder="Escolha a letra de risco")
            
            self.df_cred = self.df_cred[self.df_cred["Risco BACEN"] == risco]  

            Carteira = col2.selectbox("Carteira", self.df_cred["Carteira"].unique(), index=None, placeholder="Escolha a carteira")

            self.df_cred = self.df_cred[self.df_cred["Carteira"] == Carteira]

            Linha = col3.selectbox("Linha", self.df_cred["Linha Simplificada"].unique(), index=None, placeholder="Escolha a linha")

            self.df_cred = self.df_cred[self.df_cred["Linha Simplificada"] == Linha]
            
            #Natureza da Taxa
            self.taxa_op = m_col3.selectbox(
                'Natureza da taxa?',
                ('Pré-fixada', 'Pós-fixada'))
      
            #INAD
            self.inad_op = m_col4.selectbox(
                'Considerar o INAD?',
                ('Sim', 'Não'), index=1)

        with st.expander("Spread (%)"):
            col1, col2, col3 = st.columns([2,1,1])
            
            #Spread
            self.spread_op = col1.text_input("Spread em termos do CDI (%)",
                    "0",
                    key="spread_op")
            
            col2.metric("CDI (a.m)" , f"{self.cdi_am}%")
            col3.metric("Spread em CDI (a.m)" , f"{round((self.spread/100)*self.cdi_am,2)}%", f"{round(self.spread_CDI - self.cdi_am,2)} p.p CDI (a.m)")

        with st.expander("Redutores (%)"):
            col1, col2 = st.columns(2)
            
            #RedutorCC
            self.redutorCC_op = col1.text_input("Redutor do Custo de Crédito (%)",
                    "0", key="redutorCC_op")

            #RedutorTB  
            self.redutorTB_op = col2.text_input("Rebate da Taxa de Balcão (%)",
                    "0", key="redutorTB_op")
            
if __name__ == "__main__": 
    Precificador()