from langchain_community.llms import Ollama

def run_llama3(prompt):
    llm = Ollama(model="llama3.2")
    return llm(prompt)