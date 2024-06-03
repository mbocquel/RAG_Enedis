# RAG Enedis

On going project ..

## What do I want to do 
I want to experiment with practival use cases for LLM, Hugging Face API and LamgChain. So I decided to build a chatbot that can use RAG technique to answer questions based on Enedis official Client and Technical documentation (yes I use to work in the energy field... ) : https://www.enedis.fr/documents

### Web Scaraping 
The first step is to scrap the Enedis documentation website (https://www.enedis.fr/documents) to retrieve the list of all pdf documents available. Do to that I used BS4 library. 

### Embedding vector database
To do : 
- Read and extract the text in the pdf documents (prototype done)
- Embed the chuncks of text and store them in a vector database
- Create a LLM chain with LangChain to answer technical questions using the informations in the documents 
- Build an API and a frond end to make it nicer. 
- Deploy this app. 