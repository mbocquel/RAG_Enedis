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
- Create a chatbot with Agents : 
    - Function 1 : Search in the summary of Enedis document to give the user links to documents that can be helpfull
    - Function 2 : Download a PDF document from the Enedis website, parse it like in the RAG and answer questions about it
    - Function 3 : Send an email to the user with a summary of the conversation
    - Function 4 : Create a summary of an Enedis PDF Document
    - Function 5 : Search for client information in a database
    - Function 6 : Save the conversation in a database for use later.