from Kaggle_code_parsing import *
from LLM_summarization import *
from libraries_visualized import *
import json

def main(config):
    full_CSV_dataframe_name = f"{list(filter(bool, config['competition_url'].split('/')))[-1]}_{config['competitions_sort_by'].replace(' ', '')}_{config['competitions_amount']}.csv"
    
    Kaggle_code_parsing(config['competition_url'], config['competitions_sort_by'], config['competitions_amount'], config['CSVs_SAVE_DIR'], config['no_sublibraries'])
    LLM_summarization(config['CSVs_SAVE_DIR'] + full_CSV_dataframe_name, config['LLM_model_name'], config['LLM_temperature'], config['show_first_five'])
    building_html_graph(config['CSVs_SAVE_DIR'] + full_CSV_dataframe_name, config['GRAPH_SAVE_DIR'], config['no_sublibraries'])
    
    
def load_config_parameters():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config




if __name__ == "__main__":

    main(load_config_parameters())

