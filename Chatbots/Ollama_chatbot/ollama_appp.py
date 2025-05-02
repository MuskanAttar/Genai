import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import os

from dotenv import load_dotenv
load_dotenv()

##Langsmith tracking -- only for ref its paid
#os.environ["Langchain_api_key"]=os.getenv("langchain_api_key")
#os.environ["Langchain_Tracing_V2"]="true"
#os.environp["Langchain_project"]="Simple chatbot"

#prompt template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","you are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,llm,temperature,max_token):
    llm=Ollama(model=llm)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

# Title of app
st.title("Q&A chatbot")

##select openai model
llm=st.sidebar.selectbox("Select open AI model",["gemma:2b"])

##adjust response parameter

temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

##main interface for user input

st.write("go ahead and ask any question")
user_input=st.text_input("you:")

if user_input:
    response=generate_response(user_input,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("please ask question")

