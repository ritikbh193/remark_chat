
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.vectorstores import DocArrayInMemorySearch

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ChatMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import MessagesPlacehold







'''code 4'''
import streamlit as st
import sys
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
# from langchain.vectorstores import DocArrayInMemorySearch

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.prompts.chat import MessagesPlaceholder

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import NLTKTextSplitter
from langchain_community.vectorstores import Chroma  # Only import once

# Saving conversation history with this code
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

# Download NLTK punkt if needed
import nltk
nltk.download('punkt')  # Correct the download name



import os
# Load Google API Key from environment variable for security
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the model
model = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest', temperature=0.7, google_api_key=google_api_key)


# Set up memory and conversation chain
memory = ConversationBufferMemory()
conversation_chain = ConversationChain(llm=model, memory=memory)


# PDF loading and splitting
pdf_path = r"C:\python\Updated Remark App Description.pdf"  # Modify this to your path
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# Split the content using NLTKTextSplitter
text_splitter = NLTKTextSplitter(chunk_size=2000, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

# Embed the chunks and store them in a vector store
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)

# Create Chroma vectorstore and persist it
db = Chroma.from_documents(chunks, embedding_model, persist_directory="./chroma_db_")
db.persist()

# Connect to the Chroma vectorstore
db_connection = Chroma(persist_directory="./chroma_db_", embedding_function=embedding_model)

# Create the retriever
retriever = db_connection.as_retriever(search_kwargs={"k": 9})

# Create chat template
chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="""You are a personal assistant for user and your name is Remark. Given a context and question from the user, you should answer based on the given context and ask for more information if needed."""),
    HumanMessagePromptTemplate.from_template("""Answer the question based on the given context and ask if needed the more information also save user details like name description and more. You are a personal assistant for the Remark Job And Recruiter Portal. 
    Context: {context}

    Question: {question}
    Answer: """)
])

# Create document chain and output parser
document_chain = create_stuff_documents_chain(model, chat_template)
output_parser = StrOutputParser()

# Chain for retrieval and answering
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | chat_template
    | model
    | output_parser
)

# Streamlit app setup
st.title("ChatBot")

# Initialize session state for storing chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to delete the entire Chroma collection
def clear_chroma_db():
    # Load the vectorstore
    db = Chroma(persist_directory="./chroma_db_", embedding_function=embedding_model)
    # Delete the entire collection
    db.delete_collection()
    st.success("Deleted ")

# Function to handle chat and store response
def chat_with_remark(user_input):
    # Check if user input is 'clear' and clear the Chroma database
    if user_input.lower() == "clear":
        clear_chroma_db()  # Clear Chroma DB
        return "Chroma DB and chat history have been cleared."

    all_chunks = []
    for chunk in rag_chain.stream(user_input):
        all_chunks.append(chunk)
        sys.stdout.write(chunk)
        sys.stdout.flush()

    return ''.join(all_chunks)

# Input for user question
user_input = st.text_input("Ask a Question:", key="user_input")

# If there's user input, generate a response
if user_input:
    answer = chat_with_remark(user_input)
    st.session_state.chat_history.append({"question": user_input, "answer": answer})

# Display chat history
if st.session_state.chat_history:
    st.write("### Chat")
    for entry in st.session_state.chat_history:
        st.write(f" {entry['question']}")
        st.write(f" {entry['answer']}")
        st.write("---")

# Button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    clear_chroma_db()  # Also clear the Chroma DB when the button is clicked






'''code4.1'''
# import streamlit as st
# import sys
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain.prompts import ChatPromptTemplate
# from langchain.schema.output_parser import StrOutputParser
# # from langchain.vectorstores import DocArrayInMemorySearch

# from langchain_core.messages import SystemMessage
# from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain.chains.combine_documents import create_stuff_documents_chain
# # from langchain.prompts.chat import MessagesPlaceholder

# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import NLTKTextSplitter
# from langchain_community.vectorstores import Chroma  # Only import once

# # Saving conversation history with this code
# from langchain.chains import ConversationChain
# from langchain.chains.conversation.memory import ConversationBufferMemory

# # Download NLTK punkt if needed
# import nltk
# nltk.download('punkt')  # Correct the download name



# import os
# # Load Google API Key from environment variable for security
# google_api_key = os.getenv("GOOGLE_API_KEY")

# # Initialize the model
# model = ChatGoogleGenerativeAI(model='gemini-1.5-pro-latest', temperature=0.7, google_api_key=google_api_key)


# # Set up memory and conversation chain
# memory = ConversationBufferMemory()
# conversation_chain = ConversationChain(llm=model, memory=memory)


# # PDF loading and splitting
# pdf_path = r"C:\python\Updated Remark App Description.pdf"  # Modify this to your path
# loader = PyPDFLoader(pdf_path)
# documents = loader.load()

# # Split the content using NLTKTextSplitter
# text_splitter = NLTKTextSplitter(chunk_size=2000, chunk_overlap=100)
# chunks = text_splitter.split_documents(documents)

# # Embed the chunks and store them in a vector store
# embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)

# # Create Chroma vectorstore and persist it
# db = Chroma.from_documents(chunks, embedding_model, persist_directory="./chroma_db_")
# db.persist()

# # Connect to the Chroma vectorstore
# db_connection = Chroma(persist_directory="./chroma_db_", embedding_function=embedding_model)

# # Create the retriever
# retriever = db_connection.as_retriever(search_kwargs={"k": 9})

# # Create chat template
# chat_template = ChatPromptTemplate.from_messages([
#     SystemMessage(content="""You are a personal assistant for user and your name is Remark. Given a context and question from the user, you should answer based on the given context and ask for more information if needed."""),
#     HumanMessagePromptTemplate.from_template("""Answer the question based on the given context and ask if needed the more information. You are a personal assistant for the Remark Job And Recruiter Portal. 
#     Context: {context}

#     Question: {question}
#     Answer: """)
# ])

# # Create document chain and output parser
# document_chain = create_stuff_documents_chain(model, chat_template)
# output_parser = StrOutputParser()

# # Chain for retrieval and answering
# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | chat_template
#     | model
#     | output_parser
# )

# # Streamlit app setup
# st.title("ChatBot")

# # Initialize session state for storing chat history
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# # Function to delete the entire Chroma collection
# def clear_chroma_db():
#     # Load the vectorstore
#     db = Chroma(persist_directory="./chroma_db_", embedding_function=embedding_model)
#     # Delete the entire collection
#     db.delete_collection()
#     st.success("Deleted ")

# # Function to handle chat and store response
# def chat_with_remark(user_input):
#     # Check if user input is 'clear' and clear the Chroma database
#     if user_input.lower() == "clear":
#         clear_chroma_db()  # Clear Chroma DB
#         return "Chroma DB and chat history have been cleared."

#     all_chunks = []
#     for chunk in rag_chain.stream(user_input):
#         all_chunks.append(chunk)
#         sys.stdout.write(chunk)
#         sys.stdout.flush()

#     return ''.join(all_chunks)

# # Input for user question
# user_input = st.text_input("Ask a Question:", key="user_input")

# # If there's user input, generate a response
# if user_input:
#     answer = chat_with_remark(user_input)
#     st.session_state.chat_history.append({"question": user_input, "answer": answer})

# # Display chat history
# if st.session_state.chat_history:
#     st.write("### Chat")
#     for entry in st.session_state.chat_history:
#         st.write(f" {entry['question']}")
#         st.write(f" {entry['answer']}")
#         st.write("---")

# # Button to clear chat history
# if st.button("Clear Chat History"):
#     st.session_state.chat_history = []
#     clear_chroma_db()  # Also clear the Chroma DB when the button is clicked

























