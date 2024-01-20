import git
import os
from queue import Queue
import streamlit as st
from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationSummaryMemory
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

class Embedder:
    def __init__(self, git_link) -> None:
        self.git_link = git_link
        self.last_name = self.git_link.split('/')[-1]
        self.clone_path = self.last_name.split('.')[0]
        self.last_name = self.clone_path
        self.MyQueue =  Queue(maxsize=2)
        self.PATH = f"data/embeddings/{self.last_name}"
        

    def add_to_queue(self, value):
        if self.MyQueue.full():
            self.MyQueue.get()
        self.MyQueue.put(value)
    
    def delete_directory(self, path):
        if os.path.exists(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    os.rmdir(dir_path)
            os.rmdir(path)
        
    def load_db(self):
        #if embeddigs are saved
        if os.path.isdir(self.PATH):
            # Load the vectors from the pickle file
            self.vectors = Chroma(persist_directory=self.PATH, embedding_function=OpenAIEmbeddings(disallowed_special=()))
        else:
            #if not, clone repo and get and store embeddings
            if not os.path.exists(self.clone_path):
                # Clone the repository
                git.Repo.clone_from(self.git_link, to_path=self.clone_path)
            
            #read and store vectors
            loader = GenericLoader.from_filesystem(
                self.clone_path,
                glob="**/*",
                suffixes=[".py"],
                exclude=["**/non-utf8-encoding.py"],
                parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
            )
            documents = loader.load()

            python_splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
            )
            self.texts = python_splitter.split_documents(documents)

            self.vectors = Chroma.from_documents(self.texts, OpenAIEmbeddings(disallowed_special=()),persist_directory=self.PATH)
            
            self.delete_directory(self.clone_path)

        #get vector retriever with search type
        self.retriever = self.vectors.as_retriever(
            search_type="mmr",  # Also test "similarity"
            search_kwargs={"k": 8},
        )
        


    def retrieve_results(self, query):
        llm = ChatOpenAI(model_name=st.session_state['model'])
        memory = ConversationSummaryMemory(
            llm=llm, memory_key="chat_history", return_messages=True
        )
        qa = ConversationalRetrievalChain.from_llm(llm, retriever=self.retriever, memory=memory)
        question = query
        result = qa(question)
        return result["answer"]