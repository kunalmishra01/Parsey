import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.utils import Utils, Mappings
from modules.layout import Layout
from modules.sidebar import Sidebar

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

st.header("Coming soon! 🛠",divider='rainbow')

