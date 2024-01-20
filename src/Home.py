import streamlit as st

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

st.title("Parsey 👁")

st.markdown("---")

about, tags = st.columns(2)

with about:
    st.write("\n")
    st.write()
    st.write()
    st.write("⚡️ I am Parsey, a smart conversational agent born out of the synergy between Langchain and Streamlit.")
    st.write("⚡️ I leverage extensive language models to facilitate interactions that are sensitive to the context. My primary objective is to assist you in gaining a deeper comprehension of your data or code.")
    st.write("⚡️ I am equipped to handle *PDF, TXT, CSV* files, *Youtube* transcripts, and *code* snippets.")

with tags:
    with st.expander("Know you data!"):
        st.write("""- **Know_your_data**: General Chat on data (PDF, TXT,CSV) with a [vectorstore](https://github.com/facebookresearch/faiss) (index useful parts(max 4) for respond to the user) | works with [ConversationalRetrievalChain](https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html)""")
        st.image("static/images/data_bot.jpeg",width = 240)
    with st.expander("Know you code!"):
        st.write("""- **Know_your_code**: General Chat on code.Just submit any public git repository link  and you can ask questions regarding your code. """)
        st.image("static/images/code_bot.jpeg",width = 240)
    with st.expander("Summarize YT videos!"):
        st.write("""**Summarize_videos**: Summarize YouTube videos with [summarize-chain](https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html)""")
        st.image("static/images/yt_bot.jpeg",width = 240)
    with st.expander("Analyze data - magic pandas!"):
        st.write("""- **Analyze_data** (beta): Chat on tabular data (CSV) | for precise information | process the whole file | works with [CSV_Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/csv.html) + [PandasAI](https://github.com/gventuri/pandas-ai) for data manipulation and graph creation""")
        st.image("static/images/graph_bot.jpeg",width = 240)


st.markdown("---")

#Contributing

contact, updates= st.columns(2)
with contact:
    st.markdown("### 📞 Contact us!")
    st.write("**GitHub:**","[Parsey](https://github.com/kunalmishra01/Parsey)")
    st.write("**LinkedIn:** [@kunal](https://www.linkedin.com/in/kunalmishra210)")
    st.write("**E-Mail** : kunalmishraiitbhu@gmail.com")
with updates:
    st.markdown("### 🎯 Updates")
    st.markdown("""
    **Parsey is under regular development. Keep following for regular updates!**
    """, unsafe_allow_html=True)

   