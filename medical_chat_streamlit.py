import streamlit as st
from openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from check_db import db_check


from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
#Get Openai Key

openaikey = st.secrets["OPENAIKEY"]
embedding_function =OpenAIEmbeddings(openai_api_key=openaikey)
chat = ChatOpenAI(openai_api_key=openaikey)

# Check database.
db_check()
                           
def load_db_from_disk():
    db = Chroma(persist_directory="./medical_db", embedding_function=embedding_function)
    print(type(db))
    return db

def seach_similarity(query,db):
    docs = db.similarity_search(query)
    return docs

# Mock function to process the document and generate an answer
def openai_process(question,context):
    """Asks a question to the LLM and gets the response."""
    # Prepare the messages with the question
    messages = [
        SystemMessage(content=f"""You are a helpful medical assistant.
        You studied various medical books to give the best answer.
        Based on what you have learned, give reliable answer that can benefit to patients and your fellow doctors. Add reference to the answer in this format. Ref: Ref Name.
        Here is the context {context}"""),
        HumanMessage(content=question)
    ]

    # Execute the chat session and get the response
    response = chat(messages)

    return response.content

def handle_query(query):
    # Your logic to handle the query and search documents
    db = load_db_from_disk()
    raw_answers=seach_similarity(query,db)

    if raw_answers:
        matched_chunk = raw_answers[0]  # Assuming the first document is the most relevant
        print(matched_chunk.page_content)
        
        answer = openai_process(str(query),str(matched_chunk))  # Process the document to generate an answer
    else:
        answer = "Sorry, I couldn't find relevant information."
    return answer


def streamlit_view():
    st.title("Doctor Bot")
    with st.expander("See explanation"):
        st.markdown("""
            Developed by [Dr. Nyein Chan Ko Ko](https://www.linkedin.com/in/nchanko)
            \n
            This is a simple chatbot using RAG model to answer medical questions.
        """)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if query := st.chat_input("Ask me?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(query)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        # Generate assistant response
        with st.spinner("Thinking..."):
            answer = handle_query(query)

        # Prepare assistant response
        response = f"AI: {answer}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


streamlit_view()

