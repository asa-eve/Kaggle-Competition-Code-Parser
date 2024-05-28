import pandas as pd
import numpy as np
from collections import OrderedDict
import os
import ast

import networkx as nx
from pyvis.network import Network
import community as community_louvain

import argparse

from visualization_functions import *


#######################################################################

def building_html_graph(path_to_dataframe, SAVE_DIR, NO_SUBLIBRARIES):

    print("")
    print("============== Visual Graph Construction =================")
    print("SETTINGS")
    print(f"        Data frame path                         -   {path_to_dataframe}")
    print(f"        HTML save path                          -   {SAVE_DIR}")
    print(f"        Not to consider sublibraries            -   {'Yes'*bool(NO_SUBLIBRARIES) + 'No'*(1 - bool(NO_SUBLIBRARIES))}")
    print("")
    print("")
    
    df = pd.read_csv(path_to_dataframe)
    df['python_libraries'] = df['python_libraries'].apply(ast.literal_eval)
    
    # gathering all unique libraries
    if int(NO_SUBLIBRARIES):
        all_python_libraries = list(OrderedDict.fromkeys(sum(df['python_libraries'], [])))
        cleaned_all_python_libraries_repeated = clean_library_names(all_python_libraries)
        cleaned_all_python_libraries= list(OrderedDict.fromkeys(cleaned_all_python_libraries_repeated, []))
    else:
        all_python_libraries = list(OrderedDict.fromkeys(sum(df['python_libraries'], [])))
        cleaned_all_python_libraries = clean_sublibrary_names(all_python_libraries)
    
    
    # creating binary vector representation of libraries
    libraries_count_dict = count_strings(sum(df['python_libraries'], []), cleaned_all_python_libraries, int(NO_SUBLIBRARIES))

    df_connection = pd.DataFrame(columns=['source', 'target'])
    connection_list = []

    df_new = df.copy()
    df_new['binary_vector'] = pd.Series([np.zeros(len(libraries_count_dict), dtype=int) for _ in range(len(df_new))])
    for _, row in df_new.iterrows():
        for i, library in enumerate(libraries_count_dict):
            if library in row.python_libraries:
                row.binary_vector[i] += 1
                connection_list.append({'source': library, 'target': f'✔️ ID_{_} --- ' + row.notebook_name + ' ✔️', 'value': int(libraries_count_dict[library])}) 
                                        # TARGET --- by ID --- by notebook_name 
                                        # VALUE --- count int(libraries_count_dict[library]) --- public score

    df_connection = pd.concat([df_connection, pd.DataFrame(connection_list)], ignore_index=True)


    # making a graph
    Graph = nx.from_pandas_edgelist(df_connection,
                                   source = 'source',
                                   target = 'target',
                                   edge_attr = 'value',
                                   #title = 'LLM_summarized_code',
                                   create_using = nx.Graph())




    net = Network(notebook = True, width="1920px", height="1080px", bgcolor='#222222', font_color='white')

    node_degree = dict(Graph.degree)
    nx.set_node_attributes(Graph, node_degree, 'size')

    communities = community_louvain.best_partition(Graph)
    nx.set_node_attributes(Graph, communities, 'group')

    # Title must be a dictionary with exact name as the node 
    # I'll add only for the NOTEBOOKS
    titles = {}
    for i, name in enumerate((set(df_connection['target']))):
        titles[name] = df_new.iloc[i].LLM_summarized_code
    #titles = {'ID - 3 ---Mistral 7B Baseline - [LB 0.7X]': text}
    nx.set_node_attributes(Graph, titles, 'title')

    net.from_nx(Graph)

    competition_name, _ = os.path.splitext(os.path.basename(path_to_dataframe))
    net.show_buttons(filter_="physics") # only show physics options
    net.show(f"{SAVE_DIR}/{competition_name}.html")
    
    
#######################################################################
    
if __name__ == "__main__":
    
    # python libraries_visualized.py "Kaggle notebooks CSVs/ai-mathematical-olympiad-prize_votecount_9.csv" Graphs 1
    
    parser = argparse.ArgumentParser(description='Utilizing LLM to make a short summary for the code.')
    parser.add_argument('path_to_dataframe', type=str, help='The path to pandas data frame.')
    parser.add_argument('SAVE_DIR', type=str, help='Path where to save html"s.')
    parser.add_argument('NO_SUBLIBRARIES', type=int, help='Whether not to consider sublibraries as libraries or not. (0/1 - No/Yes)')
    
    args = parser.parse_args()
    building_html_graph(args.path_to_dataframe, args.SAVE_DIR, args.NO_SUBLIBRARIES)