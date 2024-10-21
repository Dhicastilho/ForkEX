import duckdb
class Simulacao():
    def __init__(self):
        self.conn = duckdb.connect('Data/bd_prec.db')

        # Criando a tabela de usuários, caso ainda não exista, com as colunas adicionais
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS simulacao (
                n_sim INTEGER PRIMARY KEY,
                tx_final REAL,
                tabela TEXT,
                natureza TEXT,
                risco TEXT,
                linha TEXT,
                n_linha TEXT,
                prazo TEXT,
                nome_cli TEXT,
                nome_ger TEXT,
                nome_pa TEXT,
                num_pa TEXT,
                email TEXT
            )
        ''')

    def inserir_simulacao(self, tx_final, tabela, natureza, risco, linha, n_linha, prazo, nome_cli, nome_ger, nome_pa, num_pa, email):  
        self.conn.execute('''
            INSERT INTO simulacao
            VALUES
            (
                (SELECT COALESCE(MAX(n_sim), 0) + 1 FROM simulacao),
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        ''', (tx_final, tabela, natureza, risco, linha, n_linha, prazo, nome_cli, nome_ger, nome_pa, num_pa, email))
        self.conn.commit()

    def ler_simulacao(self):    
        return self.conn.execute('SELECT * FROM simulacao').fetchall()
    
    def ler_simulacao_PorEmail(self, email):    
        return self.conn.execute('SELECT * FROM simulacao where email = ?',{email}).fetchall()

    def deletar_simulacao(self):
        self.conn.execute('DELETE FROM simulacao')  
        self.conn.commit()     
    
    def obter_simulacao(self, n_sim):
        return self.conn.execute(f'SELECT * FROM simulacao WHERE n_sim = {n_sim}').fetchall()
           