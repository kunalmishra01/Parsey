import streamlit as st
import modules.codebot_utils as utils
import os

class Codebot:
     
    @staticmethod
    def code_chat_bot_setup():
        user_repo = st.session_state['user_repo']

        with st.status("Processing your repo...", expanded=False) as status:  
            PATH = 'data/embeddings' #path to store embeddings
            if not os.path.exists(PATH):
                os.mkdir(PATH)         
            ## Load the Github Repo
            st.write("Parsing the content and embedding it. This may take some time")
            embedder = utils.Embedder(user_repo)
            embedder.load_db()
            # Initialize chat history
            st.session_state['messages'] = []
            st.write("Done Loading. Ready to take your questions")
            st.session_state['code_embedder'] = embedder
            status.update(label="Processing complete. Ask me anything about your code!", state="complete", expanded=False)

    @staticmethod
    def code_chat_bot_conversation():

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if prompt := st.chat_input("Type your question here."):
            embedder = st.session_state['code_embedder']
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            # Display assistant response in chat message container
            response = embedder.retrieve_results(prompt)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})