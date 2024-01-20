import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.utils import Utils, Mappings
from modules.layout import Layout
from modules.sidebar import Sidebar
from modules.codebot import Codebot


#set default page config on every page
st.set_page_config(
    page_title="Parsey👁",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "https://docs.streamlit.io/ ",
        'Report a bug': "https://docs.streamlit.io/",
        'About': "# This is an *parsey* , your data bot!"
    }
)

#https://python.langchain.com/docs/use_cases/code_understanding

#if any changes in modules , reload them (press R) 
utils_module = Utils.module_reload('modules.utils')
layout_module = Utils.module_reload('modules.layout')
sidebar_module = Utils.module_reload('modules.sidebar')
code_module= Utils.module_reload('modules.codebot')

Layout = layout_module.Layout
Utils = utils_module.Utils
Sidebar = sidebar_module.Sidebar
CodeBot = code_module.Codebot

# Instantiate the main components
page_map = Mappings.pages_map['code']
layout, sidebar, utils = Layout(page_map), Sidebar(page_map), Utils(page_map)
file_types = ['code snippet']
#show header
st.header("Chat with Parsey on your codebase!",divider='rainbow')

#get api key
user_api_key = Utils.load_api_key()

#start processing
if not user_api_key:
    layout.show_api_key_missing()
else:
    os.environ["OPENAI_API_KEY"] = user_api_key

    user_repo = st.text_input("Github Link to your public codebase", placeholder= "https://github.com/priya-dwivedi/exec_data_chatbot.git", key = 'user_repo', on_change=Utils.update_code_repo)
    if len(user_repo):
        # Configure the sidebar
        sidebar.show_options()
        if "code_embedder" not in st.session_state:
            Codebot.code_chat_bot_setup()
        # Accept user input
        CodeBot.code_chat_bot_conversation()

        


        
