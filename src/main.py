import os
import sys
import json

# Ensure the parent directory of src is in the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import the src package
from src.modules import *
import src


def main(config):
    full_CSV_dataframe_name = f"{list(filter(bool, config['competition_url'].split('/')))[-1]}_{config['competitions_sort_by'].replace(' ', '')}_{config['competitions_amount']}.csv"
    
    Code_parsing(config['competition_url'], config['competitions_sort_by'], config['competitions_amount'], config['CSVs_SAVE_DIR'], config['no_sublibraries'])
    LLM_summarization(config['CSVs_SAVE_DIR'] + full_CSV_dataframe_name, config['LLM_model_name'], config['LLM_temperature'], config['show_first_five'])
    building_html_graph(config['CSVs_SAVE_DIR'] + full_CSV_dataframe_name, config['GRAPH_SAVE_DIR'], config['no_sublibraries'])
    
    
def load_config_parameters():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    
    main(load_config_parameters())