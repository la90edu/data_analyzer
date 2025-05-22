import streamlit as st
import time
import llms
import pandas as pd
import llm_system_massage_manager

def response_generator(prompt, df):
    data = df.to_markdown()
    system_prompt = llm_system_massage_manager.get_first_system_prompt(data)
    response_stream = llms.get_openai_response(prompt, system_prompt, st.session_state.messages, {}, stream=True)
    
    full_response = ""
    for chunk in response_stream:
        if chunk.choices and hasattr(chunk.choices[0], "delta") and hasattr(chunk.choices[0].delta, "content"):
            content = chunk.choices[0].delta.content
            if content:
                yield content + " "
                time.sleep(0.05)
                full_response += content
    return full_response

def add_chat(data):
    st.title("Simple chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt, data))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    
# Example DataFrame
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
})

# Convert DataFrame to a string representation
data = df.to_markdown()

# Call the add_chat function with the data

# add_chat()
#     import os
# import json
# from dotenv import load_dotenv
# from openai import OpenAI
# import gradio as gr
# # Initialization

# load_dotenv(override=True)

# openai_api_key = os.getenv('OPENAI_API_KEY')
# # if openai_api_key:
# #     print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
# # else:
# #     print("OpenAI API Key not set")
    
# MODEL = "gpt-4o-mini"
# openai = OpenAI()

# system_message = "You are a helpful assistant for an Airline called FlightAI. "
# system_message += "Give short, courteous answers, no more than 1 sentence. "
# system_message += "Always be accurate. If you don't know the answer, say so."
# # This function looks rather simpler than the one from my video, because we're taking advantage of the latest Gradio updates

# def chat(message, history):
#     messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
#     response = openai.chat.completions.create(model=MODEL, messages=messages)
#     return response.choices[0].message.content

# # gr.ChatInterface(fn=chat, type="messages").launch()