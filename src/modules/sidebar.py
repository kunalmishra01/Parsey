import streamlit as st
import os
from dotenv import load_dotenv
import pdfplumber
import pandas as pd


class Sidebar:
    def __init__(self,page_map) -> None:
        self.page_map = page_map
        self.MODEL_OPTIONS = ["gpt-3.5-turbo", "gpt-4"]
        self.MODEL_OPTIONS_YT_SUMMARY = ["gpt-3.5-turbo","text-davinci-003"]
        self.TEMPERATURE_MIN_VALUE = 0.0
        self.TEMPERATURE_MAX_VALUE = 1.0
        self.TEMPERATURE_DEFAULT_VALUE = 0.0 if self.page_map!=2 else 0.7
        self.TEMPERATURE_STEP = 0.01

    @staticmethod
    def reset_chat_button():
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    def model_selector(self):
        model = st.selectbox(label="Model", options=self.MODEL_OPTIONS if self.page_map!=2 else self.MODEL_OPTIONS_YT_SUMMARY)
        st.session_state["model"] = model

    def temperature_slider(self):
        temperature = st.slider(
            label="Temperature",
            min_value=self.TEMPERATURE_MIN_VALUE,
            max_value=self.TEMPERATURE_MAX_VALUE,
            value=self.TEMPERATURE_DEFAULT_VALUE,
            step=self.TEMPERATURE_STEP,
        )
        st.session_state["temperature"] = temperature
    
    def show_options(self):
        with st.sidebar.expander("🛠️ Settings", expanded=False):
            if self.page_map!=2:
                self.reset_chat_button()
            self.model_selector()
            self.temperature_slider()
            st.session_state.setdefault("model", self.MODEL_OPTIONS[0])
            st.session_state.setdefault("temperature", self.TEMPERATURE_DEFAULT_VALUE)




        


