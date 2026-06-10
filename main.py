from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2")

#repo = "https://github.com/Jayeshraundal/stm32_custombootloader"
#question = "What is the llm?"

template = """You are a helpful assistant that answers questions about the given git repository. 
    
            Please answer the following question: {question}"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

while True:
    print("\n\n------------------------------------------------------------------")
    question = input("Enter your question (q to quit): ")
    print("\n\n")
    if question == 'q':
        break

    response = chain.invoke({"question": question})
    print(response)
    
