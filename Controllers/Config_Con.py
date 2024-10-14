import os
import yaml
current_dir = os.path.abspath(os.curdir)
file_path = os.path.join(current_dir, 'Config', 'config.yaml')
class Yaml_Con():
    def __init__(self):
        self.config = None
        
        with open(file_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)