# Kaggle Competition Code Parser
The purpose of this code is to make improving Machine Learning skills using Kaggle much easier for new people. 

It uses Large Language models (LLMs) powered by OLLAMA app in order to make summary of the code. 

Visual representation makes it easier to see which Python libraries are being mostly used by the programmers - so one can either make a list of which libraries are quite popular for which ML areas, but also look at how people approach the competition problems differently.

## More details on the project
- Parsing can be used for any competition - as long as it's from Kaggle official website
  - currently **parsing available only for Firefox browser**
  - parsing input arguments
    - `competition url` - (example: https://www.kaggle.com/competitions/titanic)
    - `sort_by` - (`public score` / `vote count` / `comment count`)
    - `amount` - (didn't explicitly defined a limit - so be careful with the amount)
    - `CSVs_SAVING_DIR` - (where to store the dataframe)
  - parsed dataframe columns (CSV)
      - example of dataframe (that will be stored after parsing)
         notebook_name | notebook_url | public_score | private_score | medal | upvotes | views | run_time_info | last_updated | notebook_full_text | code_text | markdows_text | input_datasources | python_libraries
         --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
         Example 1 |  https://www.kaggle.com/code/example_1 | 0.88 | None | silver | 105 | 1352 | 13.1s - GPU T4 x2 | 2 months | ... | ... | ... | ['competition_dataset', 'open-math-mistral'] | [torch, transformers, pandas, tqdm, gc, re, ...]
- **LLM notebooks summary using OLLAMA**
  - requires OLLAMA application to be install - since `transformers` library and local using is very time costly
  - summarization input parameters
    - `model name` - you can use any model that's available with OLLAMA ([link to the models](https://ollama.com/library))
    - `model temperature` - to regulate on how creative the LLM will be with it's answers (summaries) - the bigger, more creative [0.5 by default]
- **Visual representation using GRAPHS** (networkx & pyvis)
  - nodes - python libraries & competition notebooks
  - edges - the edge between vertices exists, if the library was used in the code
 
## 📃 File Structure
```
Kaggle-Competition-Code-Parser/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── modules/
│       ├── __init__.py
│       ├── Kaggle_code_parsing.py
│       ├── LLM_summarization.py
│       ├── libraries_visualized.py
│       ├── parsing_functions.py
│       └── visualization_functions.py
├── Graphs/
├── Kaggle notebooks CSVs/
├── config.json
├── requirements.txt
├── README.md
└── .gitignore
```
