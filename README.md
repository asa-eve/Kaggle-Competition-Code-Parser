# Kaggle Competition Code Parser
The purpose of this code is to make improving Machine Learning skills using Kaggle much easier for new people. It uses Large Language models (LLMs) powered by OLLAMA app in order to make summary of the code. Visual representation makes it easier to see which Python libraries are being mostly used by the programmers - so one can either make a list of which libraries are quite popular for which ML areas, but also look at how people approach the competition problems differently.

## 
- The code parses notebooks from chosen Kaggle competition
 - arguments: `competition url`, `sort_by`, `amount`
- Then all libraries are visually represented using graph 
 - nodes are `python libraries used` and `competitions`
 - edge between vertices exists - if the library was used in the code
 
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
