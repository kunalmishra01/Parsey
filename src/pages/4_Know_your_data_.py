import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.utils import Utils, Mappings
from modules.layout import Layout
from modules.sidebar import Sidebar
from modules.history import ChatHistory

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
history_module = Utils.module_reload('modules.history')

Layout = layout_module.Layout
Utils = utils_module.Utils
Sidebar = sidebar_module.Sidebar
ChatHistory = history_module.ChatHistory

# Instantiate the main components
page_map = Mappings.pages_map['data']
layout, sidebar, utils = Layout(page_map), Sidebar(page_map), Utils(page_map)
file_types = ['PDF','CSV','TXT']
#show header
st.header(
            f"""Ask Parsey about your {','.join(file_types)}! 😁""",divider='rainbow'
        )


#get api key
user_api_key = Utils.load_api_key()

#start processing
if not user_api_key:
    layout.show_api_key_missing()
else:
    os.environ["OPENAI_API_KEY"] = user_api_key
    st.markdown("  \n  ")
    if st.button("I'm Bored!"):
        st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")
    uploaded_file = utils.handle_file_upload(file_types)

    if uploaded_file:
        # Configure the sidebar -- set model , temperature values , add reset chat button
        sidebar.show_options()

        # Set up chat history
        history = ChatHistory()
        try:
            pass
            chatbot = utils.setup_chatbot(
                uploaded_file, st.session_state["model"], st.session_state["temperature"]
            )
            st.session_state["chatbot"] = chatbot

            if st.session_state["ready"]:
                # Create containers for chat responses and user prompts
                response_container, prompt_container = st.container(), st.container()

                with prompt_container:
                    # Display the prompt form - ready when user enters value and presses submit button
                    is_ready, user_input = utils.prompt_form()

                    # Initialize the chat history only if not already present in session state
                    history.initialize(uploaded_file)

                    # Reset the chat history if button clicked
                    if st.session_state["reset_chat"]:
                        history.reset(uploaded_file)

                    if is_ready:
                        # Update the chat history and display the chat messages
                        history.append("user", user_input)

                        old_stdout = sys.stdout
                        sys.stdout = captured_output = StringIO()

                        output = st.session_state["chatbot"].conversational_chat(user_input)

                        sys.stdout = old_stdout

                        #update response history of assistant
                        history.append("assistant", output)

                        # Clean up the agent's thoughts to remove unwanted characters
                        thoughts = captured_output.getvalue()
                        cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                        cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                        # Display the agent's thoughts
                        with st.expander("Display the agent's thoughts"):
                            st.write(cleaned_thoughts)

                history.generate_messages(response_container)
        except Exception as e:
            st.error(f"Error: {str(e)}")

