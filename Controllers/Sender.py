import win32com.client as win32
import os
import datetime as dt
import pythoncom
from Controllers.Config_Con import Yaml_Con


class Sender_email(Yaml_Con):
    def __init__(self, nome_cooperado, linha, taxa, email):
        Yaml_Con.__init__(self)
        pythoncom.CoInitialize()
        self.outlook = win32.Dispatch('outlook.application')
        self.nome_cooperado = nome_cooperado
        self.linha = linha
        self.taxa = taxa
        self.email = email
        
        try:
            current_dir = os.path.abspath(os.curdir)
            self.file_path = os.path.join(current_dir, 'Export', self.email  ,f'Simulação_{nome_cooperado[:20]}.pdf')
        except:
            print("Falhar ao carregar o anexo")
            
        try:
            current_dir = os.path.abspath(os.curdir)
            self.file_path_desc = os.path.join(current_dir, 'Export', self.email ,f'Simulação_com_desc_{nome_cooperado[:20]}.pdf')
        except:
            print("Falhar ao carregar o anexo")

        self.hora = dt.datetime.now()
        self.hora = self.hora.strftime("%H:%M:%S %d-%m-%Y")

    def enviar(self):
        i = 1
        
        for nome, email_dest in self.config["Contatos"][0].items():
        
            assunto = f"{self.nome_cooperado} | Simulação de Taxa para a linha: {self.linha} | Posição {self.hora}"
            conteudo = f"""Segue a solicitação de Precificação de Taxa Ordinária na Posição: {self.hora}! 
            <p style='font-family:Montserrat; font-size:110%'> Linha Solicitada: {self.linha} com a taxa de:{self.taxa}</p>
            <p style='font-family:Montserrat; font-size:110%'> Cooperado Solicitante: {self.nome_cooperado} | </p>
            """
            email = self.outlook.CreateItem(0)
            
            email.To = email_dest
            email.Subject = assunto
            
            email.HTMLBody = f"""
            <p style='font-family:Montserrat; font-size:110%'> Prezado, {nome}!</p>
            <p style='font-family:Montserrat; font-size:110%'> {conteudo}</p>
            <p style='font-family:Montserrat; font-size:110%'> </p>
            """
            
            email.Attachments.Add(self.file_path)
                
            email.Send()
            print(f"Email Nº {i} para {nome} {email_dest} Enviado com sucesso! [OK]", "default")
            i += 1
            
    def enviar_com_desconto(self, tx_desconto):
        i = 1
        
        for nome, email_dest in self.config["Contatos"][0].items():
        
            assunto = f"{self.nome_cooperado} | Simulação de Taxa com Desconto para a linha: {self.linha} | Posição {self.hora}"
            
            conteudo = f"""Segue a solicitação de Precificação de Taxa Extraordinária com Desconto na Posição: {self.hora}! 
            <p style='font-family:Montserrat; font-size:110%'> Desconto de {tx_desconto}% para a Linha: {self.linha}</p>
            <p style='font-family:Montserrat; font-size:110%'> Cooperado Solicitante: {self.nome_cooperado} | </p>
            """
            email = self.outlook.CreateItem(0)
            
            email.To = email_dest
            email.Subject = assunto
            
            email.HTMLBody = f"""
            <p style='font-family:Montserrat; font-size:110%'> Prezado, {nome}!</p>
            <p style='font-family:Montserrat; font-size:110%'> {conteudo}</p>
            <p style='font-family:Montserrat; font-size:110%'> </p>
            """
            email.Attachments.Add(self.file_path_desc)
                
            email.Send()
            print(f"Email Nº {i} para {nome} {email_dest} Enviado com sucesso! [OK]", "default")
            i += 1