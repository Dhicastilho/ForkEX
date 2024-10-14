import os
class Tratar_Arquivos():
    def __init__(self):
        current_dir = os.path.abspath(os.curdir)
        dir_path = os.path.join(current_dir, 'Export')
        for arquivo in os.listdir(dir_path):
            try:
                os.remove(os.path.join(dir_path, arquivo))
            except (FileNotFoundError, PermissionError):
                 continue