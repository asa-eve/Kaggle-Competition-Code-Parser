## Kaggle Competition Code Parser - LLM summarizer - Library visualizer
The purpose of this code is to make improving Machine Learning skills using Kaggle much easier for new people. 

- **Parsing** (only for Firefox) - Python code using Selenium to get valuable information (public score, private score, upvotes, views, etc.)
- **Code Summarization** - based on Large Language models (LLMs) powered by OLLAMA desktop app
- **Libraries Visualization** - graph representation using Louvain method (for community detection)

This project is a merely portfolio one - so I do not intend on improving or updating it in any way (for now).

## **Parsing (data)** - [Selenium, Requests, Nbformat]
Any competition can be parsed - as long as it's from Kaggle official website & not a closed type (means everyone can participate).

**IMPORTANT INFORMATION**:
- **ONLY for Firefox** browser
- parsing input arguments
  - `competition url` - (example: https://www.kaggle.com/competitions/titanic)
  - `sort_by` - 'public score', 'vote count', 'comment count' - these options only
  - `amount` - no limit implemented (careful)
  - `CSVs_SAVING_DIR` - path to store dataframe

**EXAMPLE**:
   notebook_name | notebook_url | public_score | private_score | medal | upvotes | views | run_time_info | last_updated | notebook_full_text | code_text | markdows_text | input_datasources | python_libraries
   --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
   Example 1 |  https://www.kaggle.com/code/example_1 | 0.88 | None | silver | 105 | 1352 | 13.1s - GPU T4 x2 | 2 months | ... | ... | ... | ['competition_dataset', 'open-math-mistral'] | [torch, transformers, pandas, tqdm, gc, re, ...]
      
## **LLM notebooks summary** - [OLLAMA]
Uses OLLAMA desktop application & python library - in order to create a short summary of each code from the dataframe. The decision of using this approach is deeply correlated with the requirements and speed, when using LLMs locally with 'transformers' library.

**The following LLM output will be saved in dataframe and used in VISUALIZATION GRAPH section.**

**INPUTS**:
- `model name` - any model that's available to OLLAMA ([link to the models](https://ollama.com/library))
- `model temperature` - regulation of "creativity" of the LLMs answers - the bigger, more creative [0.5 by default]

**DEVELOPER'S NOTE**:
- I'm not very good at prompt engineering - so you might consider IMPROVING the prompt and instructions as you like
- This part was made purely for saving time - I wasn't trying to push the limits, nor do I have enough memory to try bigger LLM models (14B, 70B parameters)
- If you have access to OpenAI ChatGPT key - I suggest you do that, since it's quite good in terms of following user's instructions.

## **Visual graph representation** - [networkx & pyvis]
In order to build a graph, Louvain method (for community detection) was used. It allows to better distinguish code without analyzing it through, but based on Python libraries only.

**INFO**:
- `NODES` - python libraries & competition notebooks
- `EDGES` - the edge between vertices exists, if the library was used in the code
- `WEIGHT`

**LLM SUMMARY**:
- when pointing at the 'competition notebook' node - you will have a summary (generated on the previous step), so you can study it and decide, whether you want to spend your time on checking out certain notebooks (without looking in them)

## Installation & Usage

 
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
