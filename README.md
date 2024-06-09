# RAG Enedis

This project is an exploration of LLM, LangChain and RAG. I created a streamlit applicaton where you can select a document from the enedis PDF library : https://www.enedis.fr/documents

## What the program does : 
- Download the file
- Transform the pdf file into a FAISS vector database. 
- Transform the question into a vector and does a similarity search with the database. 
- Create a RAG LangChain with a specific prompt template (see in config/CFG.py)
- Send the request to the Mistral / HuggingFace API
- Show the result

## Run the program 
```
make install && make get_list && make run_app
```

### Select a document and ask a question
<div align="center">
<img src="img/EnedisRAG1.png" alt="EnedisRAG1"/>
</div>

### Get your answer ! 

<div align="center">
<img src="img/EnedisRAG2.png" alt="EnedisRAG1"/>
</div>


### Web Scaraping 
The first step is to scrap the Enedis documentation website (https://www.enedis.fr/documents) to retrieve the list of all pdf documents available. Do to that I used BS4 library. 

### Features that will be implemented soon
- Use a streaming chain to reduce the waiting time
- Create other pages in the app with a chatbot able to look into a mock client database (experimenation with Agents)

