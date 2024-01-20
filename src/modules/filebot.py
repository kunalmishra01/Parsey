import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback

import langchain
langchain.verbose = False

class Chatbot:

    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors # vector with doc embeddings

    qa_template = """Your are Parsey, a intelligent chatbot. Use the following pieces of context to answer the question at the end.
                    If you don't know the answer, just say that you don't know, don't try to make up an answer.
                    Also, if the question does not belong to the given context, just say that you are not allowed to answer questions not related to the document.
                    Use three sentences minimum and keep the answer as concise as possible.

                    {context}

                    Question: {question}

                    Helpful Answer:"""

    QA_PROMPT = PromptTemplate.from_template(qa_template)

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        retriever = self.vectors.as_retriever()


        chain = ConversationalRetrievalChain.from_llm(llm=llm,
            retriever=retriever,
              verbose=True,
                return_source_documents=False,
                  max_tokens_limit=4097,
                    combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"question": query, "chat_history": st.session_state["history"]}
        result = chain(chain_input)

        st.session_state["history"].append((query, result["answer"]))
        # count_tokens_chain(chain, chain_input)
        return result["answer"]


def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        st.write(f'###### Tokens used in this conversation : {cb.total_tokens} tokens')
    return result 

    
    
