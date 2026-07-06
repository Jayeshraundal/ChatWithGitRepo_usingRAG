import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0 
)

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