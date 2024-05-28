import ollama
import pandas as pd
import argparse

##########################################################################

def validate_response(response):
    # Check for the presence of required sections
    if "Unique aspects:" not in response or "Steps taken:" not in response or "Summary:" not in response:
        return False
    
    return True


def check_results(df):
    for _, row in df.iterrows():
        print("_____________________________________________")
        print(f"Code {_}/{len(df)}")
        print("")
        print(df.iloc[_].LLM_summarized_code)
    for i in range(3): print("")

##########################################################################

def LLM_summarization(path_to_dataframe, LLM_model_name='llama3', LLM_temperature=0.5, show_first_five=False):
    
    print("")
    print("============== LLM summarization (ollama models ONLY) =================")
    print("SETTINGS")
    print(f"        Data frame path                  -   {path_to_dataframe}")
    print(f"        LLM model name                   -   {LLM_model_name}")
    print(f"        LLM temperature (creativity)     -   {LLM_temperature}")
    print(f"        Check the results for first 5    -   {'Yes'*show_first_five + 'No'*(1-show_first_five)}")
    print("")
    print(f"  !!!!!!    DON'T FORGET TO START 'OLLAMA' FIRST    !!!!!!")
    print("")
    
    df = pd.read_csv(path_to_dataframe)
    LLM_summarized_code = []
    for _, row in df.iterrows():

        print(f"Summarizing {_+1}/{len(df)} code...")

        prompt = f"""
        You are an AI assistant tasked with summarizing unique aspects of Machine Learning code written in Python.
        Your response must have: "Unique aspects", "Steps taken", "Summary".
        Strictly adhere to the provided instructions and format.

        Instructions:
        1. Your summary must be less than 100 words.
        2. Focus only on the main points of the code that make it special or unique. Avoid general steps like "downloading data" or "training the model" unless they are done in a unique way.
        3. If the Machine Learning code does not have any uniqueness in it - mention and highlight it.
        4. If the Machine Learning code has no logical connection in its steps (stolen from somewhere) - mention and highlight it.
        5. If there are no unique aspects or logical steps, provide a brief note about it.
        6. Do not include any introductory or closing phrases.

        Format your response exactly like this:

            Unique aspects:
            1. [Describe unique aspect 1]
            2. [Describe unique aspect 2]
            (Continue as necessary)

            Steps taken:
            1. [Step 1]
            2. [Step 2]
            (Continue as necessary)

            Summary:
            [Provide a brief summary highlighting the unique aspects of the code]


        Example:

            Unique aspects:
            1. The use of MMOS-DeepSeekMath-7B, a zero-shot machine learning model for mathematical reasoning.
            2. The integration of self-consistency and generated code reasoning evaluation to improve arithmetic hallucinations.

            Steps taken:
            1. Import necessary libraries, including PyTorch and transformers.
            2. Load the pre-trained MMOS-DeepSeekMath-7B model and tokenizer.
            3. Define a custom pipeline for text generation using the transformers library.
            4. Process the output of the pipeline to extract code blocks and execute them to obtain results.
            5. Integrate natural language reasoning with programs to solve mathematical problems.
            6. Use self-consistency and generated code reasoning evaluation to improve arithmetic hallucinations.

            Summary:
            This code uses MMOS-DeepSeekMath-7B, a zero-shot machine learning model for mathematical reasoning, to integrate natural language reasoning with programs to solve mathematical problems. It also employs self-consistency and generated code reasoning evaluation to improve arithmetic hallucinations.

        The following Machine Learning code for summarization:
        {row.notebook_full_text}
        """

    #     The following Machine Learning code for summarization:
    #     {row.code_text}

    #     The markdowns made by the author of the code that you might find helpful:
    #     {row.markdowns_text}

    # more of options - https://github.com/ollama/ollama/blob/main/docs/api.md

        #generated_response = ''
        #while not validate_response(generated_response):
            #generated_response = response['message']['content']

        response = ollama.chat(model=LLM_model_name, messages=[
            {
                #"seed": 42,
                "temperature": int(LLM_temperature),  # [0, 1]  (1 - extremly creative)
                'role': 'user',  # user / system
                'content': f'{prompt}',
                'stream': False,  # something related to output format
            },
        ])

        LLM_summarized_code.append(response['message']['content'])

        
    if show_first_five:
        check_results(df.assign(LLM_summarized_code=LLM_summarized_code).copy())
        
        
    print("")
    print("DONE")
    print("=======================================================================")
    
    df.assign(LLM_summarized_code=LLM_summarized_code).copy().to_csv(path_to_dataframe, index=False)


##########################################################################


if __name__ == "__main__":
    
    # python LLM_summarization.py "Kaggle notebooks CSVs/ai-mathematical-olympiad-prize_votecount_9.csv" llama3 0.5 0
    
    parser = argparse.ArgumentParser(description='Utilizing LLM to make a short summary for the code.')
    parser.add_argument('path_to_dataframe', type=str, help='The path to pandas data frame.')
    parser.add_argument('LLM_model_name', type=str, help='The name of the model from "ollama" Python library. (llama3 by default)')
    parser.add_argument('LLM_temperature', type=float, help='The temperature of LLM model. [0.5 by default]')
    parser.add_argument('show_first_five', type=int, help='Show the first 5 results.')
    
    args = parser.parse_args()
    LLM_summarization(args.path_to_dataframe, args.LLM_model_name, args.LLM_temperature, args.show_first_five)