from parsing_functions import *
from visualization_functions import clean_library_names
import argparse
import os
import ast

###############################################################################################################  

def Kaggle_code_parsing(competition_url, SORT_BY, NOTEBOOKS_AMOUNT, CSVs_SAVING_DIR, NO_SUBLIBRARIES):
    
    for i in range(8): print("")
    print("")
    print("============== KAGGLE CODE PARSING (Firefox browser ONLY) =================")
    print("SETTINGS")
    print(f"        Competition url        -   {competition_url}")
    print(f"        Sorting by             -   {SORT_BY}")
    print(f"        Amount of notebooks    -   {NOTEBOOKS_AMOUNT}")
    print(f"        Save to directory      -   {CSVs_SAVING_DIR}")
    print(f"        Remove sublibraries    -   {'Yes'*bool(NO_SUBLIBRARIES) + 'No'*(1 - bool(NO_SUBLIBRARIES))}")
    print("")
    
    
    file_name = list(filter(bool, competition_url.split('/')))[-1]
    full_file_name = f"{file_name}_{SORT_BY.replace(' ', '')}_{NOTEBOOKS_AMOUNT}.csv"

    if os.path.exists(CSVs_SAVING_DIR + full_file_name):
        print("Loading existing file")
        df = pd.read_csv(CSVs_SAVING_DIR + full_file_name)

        # transform LISTS columns into LISTS (since saving transforms them into STRINGS)
        df['python_libraries'] = df['python_libraries'].apply(ast.literal_eval)
        df['input_datasources'] = df['input_datasources'].apply(ast.literal_eval)
    else:
        print("Parsing data from competition + Saving")
        print("-----------------------------")

        df = PARSING_COMPETITION_NOTEBOOKS(competition_url, SORT_BY, True, True, NOTEBOOKS_AMOUNT)  # COMPETITION_URL / SORT_BY / PYTHON_ONLY / excludeNonAccessedDatasources / NOTEBOOKS_AMOUNT

        df.to_csv(CSVs_SAVING_DIR + full_file_name, index=False)
        
        
    if bool(int(NO_SUBLIBRARIES)):
        # changed a little big --- now 'gemma.config' considered as 'gemma' library (previously it wasn't considered at all)

        all_python_libraries = list(OrderedDict.fromkeys(sum(df['python_libraries'], [])))
        cleaned_all_python_libraries_repeated = clean_library_names(all_python_libraries)
        cleaned_all_python_libraries= list(OrderedDict.fromkeys(cleaned_all_python_libraries_repeated, []))
        print("        TOTAL AMOUNT OF LIBRARIES = ", len(cleaned_all_python_libraries))

    else:
        all_python_libraries = list(OrderedDict.fromkeys(sum(df['python_libraries'], [])))
        cleaned_all_python_libraries = clean_sublibrary_names(all_python_libraries)
        print("        TOTAL AMOUNT OF LIBRARIES + SUB-LIBRARIES = ", len(cleaned_all_python_libraries))
        
    print("")
    print("DONE")
    print("===========================================================================")
        
        
###############################################################################################################  

# SORT_BY = 'vote count' # 'public score', 'vote count', 'comment count'
# NOTEBOOKS_AMOUNT = 10
# competition_url = "https://www.kaggle.com/competitions/ai-mathematical-olympiad-prize" #"https://www.kaggle.com/competitions/llm-prompt-recovery"
# CSVs_SAVING_DIR = "Kaggle notebooks CSVs/"
# NO_SUBLIBRARIES = True
    
    
if __name__ == "__main__":
    
    # python Kaggle_code_parsing.py https://www.kaggle.com/competitions/ai-mathematical-olympiad-prize "vote count" 9 "Kaggle notebooks CSVs/" 0
    
    parser = argparse.ArgumentParser(description='Parse code from a URL and save the results. (Firefox browser ONLY)')
    parser.add_argument('url', type=str, help='The URL to fetch the code from.')
    parser.add_argument('sort_by', type=str, help='The criterion to sort the code by.')
    parser.add_argument('amount', type=int, help='The amount of code to parse.')
    parser.add_argument('saving_dir', type=str, help='The directory to save the resulting data frame.')
    parser.add_argument('no_sublibraries', type=bool, help='Whether NOT to include sublibraries in the total libraries list or not. (0/1 - No/Yes)')

    args = parser.parse_args()
    Kaggle_code_parsing(args.url, args.sort_by, args.amount, args.saving_dir, args.no_sublibraries)