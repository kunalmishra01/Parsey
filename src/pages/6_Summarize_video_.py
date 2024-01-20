import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.utils import Utils, Mappings
from modules.layout import Layout
from modules.sidebar import Sidebar
from modules.ytbot import YTBot


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

#if any changes in modules , reload them (press R) 
utils_module = Utils.module_reload('modules.utils')
layout_module = Utils.module_reload('modules.layout')
sidebar_module = Utils.module_reload('modules.sidebar')
yt_module = Utils.module_reload('modules.ytbot')

Layout = layout_module.Layout
Utils = utils_module.Utils
Sidebar = sidebar_module.Sidebar
YTBot = yt_module.YTBot

# Instantiate the main components
page_map = Mappings.pages_map['video']
layout, sidebar, utils = Layout(page_map), Sidebar(page_map), Utils(page_map)
file_types = ['YT video']

#show header
st.header(
    f"""Ask Parsey to summarize your {','.join(file_types)}! 😁""",divider='rainbow'
)

#https://blog.streamlit.io/langchain-tutorial-3-build-a-text-summarization-app/

def get_video_summary():
        video_url = st.session_state.get("video_url", None)
        with st.container():
            if video_url:
                try:
                    transcript, language_code = YTBot.get_transcript(video_url)
                    model_name = st.session_state["model"]
                    temperature = st.session_state["temperature"]
                    result = YTBot.summarize_with_langchain_and_openai(transcript,language_code,model_name,temperature)
                    st.snow()
                    st.session_state['yt_summary'] = result
                except Exception as e:
                    st.session_state['yt_summary']  = "🚨 Uhh! Failed to generate summary. Please check your URL or try a different video."

with st.container():

    #get api key
    user_api_key = Utils.load_api_key()


    #start processing
    if not user_api_key:
        layout.show_api_key_missing()
    else:
        os.environ["OPENAI_API_KEY"] = user_api_key
        sidebar.show_options()
        video_url = st.text_input("Enter Youtube Video URL", placeholder="https://www.youtube.com/watch?v=5g1LtbCtVhs", label_visibility="visible",on_change=get_video_summary, key='video_url')
        if video_url and 'yt_summary' in st.session_state:
             st.write(st.session_state['yt_summary'])
             st.title("Want to watch?")
             space,video,space = st.columns(3)
             with space:
                 st.write(" ")
             with video:
                st.write("\n\n")
                st.video(data = video_url)
             with space:
                st.write(" ")