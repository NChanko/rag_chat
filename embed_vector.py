from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from medchat import openaikey

def process_documents(directory, db=None, has_new_docs=False):
    loader = DirectoryLoader(directory, glob="./*.txt", loader_cls=TextLoader)
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splitted_documents = text_splitter.split_documents(raw_documents)

    if not db:
        # Initialize the database if it's not provided
        db = Chroma.from_documents(splitted_documents, OpenAIEmbeddings(openai_api_key=openaikey), persist_directory="./medical_db")
    elif has_new_docs:
        # Update the database with new documents
        # This step assumes `db` has a method like `add_documents` for adding new documents
        db.add_documents(splitted_documents)

    return db

# Adding new documents
process_documents('./new_books/', has_new_docs=True)
