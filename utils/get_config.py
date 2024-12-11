import yaml
from yaml import Loader


# Чтение config.yml
def load_config() -> Loader:
    with open("config.yml", encoding='utf-8') as file:
        return yaml.safe_load(file)
