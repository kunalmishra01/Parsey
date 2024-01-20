import os
import re
import openai
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document


class YTBot:

    def get_youtube_id(url):
        video_id = None
        match = re.search(r"(?<=v=)[^&#]+", url)
        if match :
            video_id = match.group()
        else : 
            match = re.search(r"(?<=youtu.be/)[^&#]+", url)
            if match :
                video_id = match.group()
        return video_id
    
    def get_transcript(youtube_url):
        
        try:
            video_id = YTBot.get_youtube_id(youtube_url)
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_manually_created_transcript()
            language_code = transcript.language_code  # Save the detected language
        except:
            # If no manual transcript is found, try fetching an auto-generated transcript in a supported language
            try:
                generated_transcripts = [trans for trans in transcript_list if trans.is_generated]
                transcript = generated_transcripts[0]
                language_code = transcript.language_code  # Save the detected language
            except:
                # If no auto-generated transcript is found, raise an exception
                st.session_state['yt_summary_error'] = "No suitable transcript found.Check your URL!"

        full_transcript = " ".join([part['text'] for part in transcript.fetch()])
        return full_transcript, language_code  # Return both the transcript and detected language

    def summarize_with_langchain_and_openai(transcript, language_code, model_name='gpt-3.5-turbo', temperature=1):
        # Instantiate the LLM model
        llm = OpenAI(temperature=temperature)
        # Split text
        text_splitter = CharacterTextSplitter()
        texts = text_splitter.split_text(transcript)
        # Create multiple documents
        docs = [Document(page_content=t) for t in texts]
        # Text summarization
        chain = load_summarize_chain(llm, chain_type='map_reduce')
        return chain.run(docs)

            
            

