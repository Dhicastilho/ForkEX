import os
class Lidar_Dir():
    def __init__(self, nome_dir_email):
        self.nome_dir_email = nome_dir_email
        current_dir = os.path.abspath(os.curdir)
        self.dir_path = os.path.join(current_dir, 'Export', self.nome_dir_email)
        
        self.criar_dir()
        
    def criar_dir(self):
        # Cria o diretório, se ele não existir
        os.makedirs(self.dir_path, exist_ok=True)
    def limpar_dir(self):
        for arquivo in os.listdir(self.dir_path):
            try:
                os.remove(os.path.join(self.dir_path, arquivo))
            except (FileNotFoundError, PermissionError):
                 continue