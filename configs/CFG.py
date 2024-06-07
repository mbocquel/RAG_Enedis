"""
CONFIG FILE FOR THE PROJECT
"""

CFG = {
    "llm": {
        "repo_id": "mistralai/Mixtral-8x7B-Instruct-v0.1", 
        "temperature":0.1, 
        "max_new_tokens": 2000
    }, 
    "chain": {
        "chain_type":"stuff", 
        "verbose": True, 
        "result_french": True
    }
}