import streamlit as st
import os
from dotenv import load_dotenv
import pdfplumber
import pandas as pd
import re

from modules.filebot import Chatbot
from modules.embedder import Embedder

class Mappings:
    pages_map = {'data' : 0,
                 'code':  1,
                 'video': 2,
                 'data_analysis': 3}
    
class Utils:

    def __init__(self,page_map) -> None:
        self.page_map = page_map
    
    @staticmethod
    def load_api_key():
        """
        Loads the OpenAI API key from the .env file or 
        from the user's input and returns it
        """
        if not hasattr(st.session_state, "api_key"):
            st.session_state.api_key = None

        if st.session_state.api_key is not None:
            user_api_key = st.session_state.api_key
            st.sidebar.success("API key loaded from previous input", icon="🚀")
            return user_api_key

        #you can define your API key in .env directly
        if os.path.exists(".env"):
            load_dotenv()
            if os.getenv("OPENAI_API_KEY") is not None:
                user_api_key = os.environ["OPENAI_API_KEY"]
                st.sidebar.success("API key loaded from .env", icon="🚀")
                return user_api_key     
        
        user_api_key = st.sidebar.text_input(
            label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
        )
        if user_api_key:
            st.session_state.api_key = user_api_key

        return user_api_key
    
    @staticmethod
    def handle_file_upload(file_types):
        """
        Handles and display uploaded_file
        :param file_types: List of accepted file types, e.g., ["csv", "pdf", "txt"]
        """
        uploaded_file = st.sidebar.file_uploader("upload", type=file_types, label_visibility="collapsed")
        if uploaded_file is not None:

            def show_csv_file(uploaded_file, nrows = 10):
                file_container = st.expander("Your CSV file (first 10 rows):")
                uploaded_file.seek(0)
                shows = pd.read_csv(uploaded_file, nrows=nrows)
                file_container.dataframe(shows)

            def show_pdf_file(uploaded_file):
                file_container = st.expander("Your PDF file :")
                with pdfplumber.open(uploaded_file) as pdf:
                    pdf_text = ""
                    for page in pdf.pages:
                        pdf_text += page.extract_text() + "\n\n"
                file_container.write(pdf_text)
            
            def show_txt_file(uploaded_file):
                file_container = st.expander("Your TXT file:")
                uploaded_file.seek(0)
                content = uploaded_file.read().decode("utf-8")
                file_container.write(content)
            
            def get_file_extension(uploaded_file):
                return os.path.splitext(uploaded_file)[1].lower()
            
            file_extension = get_file_extension(uploaded_file.name)

            # Show the contents of the file based on its extension
            if file_extension == ".csv" :
               show_csv_file(uploaded_file)
            if file_extension== ".pdf" : 
                show_pdf_file(uploaded_file)
            elif file_extension== ".txt" : 
                show_txt_file(uploaded_file)
            
        else:
            st.session_state["reset_chat"] = True

        #print(uploaded_file)
        return uploaded_file

    @staticmethod
    def update_code_repo():
        if "code_embedder" in st.session_state:
            del st.session_state["code_embedder"]


    
       
    @staticmethod
    def module_reload(module_name):
        """function to reload modules"""
        import importlib
        import sys
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
        return sys.modules[module_name]
    
    @staticmethod
    def setup_chatbot(uploaded_file, model, temperature):
        """
        Sets up the chatbot with the uploaded file, model, and temperature
        """
        embeds = Embedder()

        with st.spinner("Processing..."):
            uploaded_file.seek(0)
            file = uploaded_file.read()
            # Get the document embeddings for the uploaded file
            vectors = embeds.getDocEmbeds(file, uploaded_file.name)
            # Create a Chatbot instance with the specified model and temperature
            chatbot = Chatbot(model, temperature,vectors)
        st.session_state["ready"] = True
        return chatbot
    
    def prompt_form(self):
        """
        Displays the prompt form
        """
        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_area(
                "Query:",
                placeholder="Ask me anything about file...",
                key="input",
                label_visibility="collapsed",
            )
            submit_button = st.form_submit_button(label="Submit")
            
            is_ready = submit_button and user_input
        return is_ready, user_input