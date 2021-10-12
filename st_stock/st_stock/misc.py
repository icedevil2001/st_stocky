
import yaml


def load_cypto_symbols():
    with open('st_stock/st_stock/assets/cypto_list.txt', 'r') as symbols:
        return [symbol.strip() for symbol in symbols]

def load_config():
    with open('st_stock/st_stock/config/config.yml', 'r') as fh:
        return yaml.safe_load(fh)
