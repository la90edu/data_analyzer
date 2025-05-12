import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import llm_system_massage_manager
import pandas

def put_chatbot(data):
    
    df_markdown = data.to_markdown()

    # system_prompt=llm_system_massage_manager.first

    # initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

        st.session_state.messages.append(SystemMessage(system_prompt))#llm_system_massage_manager.first))#+ "this is the data of the school:"+df_markdown)

# display chat messages from history on app rerun
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)

# create the bar where we can type messages
    prompt = st.chat_input("How are you?")

# did the user submit a prompt?
    if prompt:

    # add the message from the user (prompt) to the screen with streamlit
        with st.chat_message("user"):
            st.markdown(prompt)

            st.session_state.messages.append(HumanMessage(prompt))

    # create the echo (response) and add it to the screen

        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
        )

        result = llm.invoke(st.session_state.messages).content

        with st.chat_message("assistant"):
            st.markdown(result)

            st.session_state.messages.append(AIMessage(result))




# import streamlit as st
# from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
# import openai  # Import OpenAI library
# import os

# # Set your OpenAI API key
# openai.api_key = os.environ.get("OPENAI_API_KEY")

# st.title("Chatbot")

# # initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # display chat messages from history on app rerun
# for message in st.session_state.messages:
#     if isinstance(message, HumanMessage):
#         with st.chat_message("user"):
#             st.markdown(message.content)
#     elif isinstance(message, AIMessage):
#         with st.chat_message("assistant"):
#             st.markdown(message.content)

# # create the bar where we can type messages
# prompt = st.chat_input("How are you?")

# # did the user submit a prompt?
# if prompt:
#     # add the message from the user (prompt) to the screen with streamlit
#     with st.chat_message("user"):
#         st.markdown(prompt)

#         st.session_state.messages.append(HumanMessage(prompt))

#     # generate a response using OpenAI GPT-4
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4o-mini",
#             messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             *[
#                 {"role": "user" if isinstance(msg, HumanMessage) else "assistant", "content": msg.content}
#                 for msg in st.session_state.messages
#             ],
#             {"role": "user", "content": prompt},
#             ],
#         )
#         assistant_message = response.choices[0].message.content

#     except Exception as e:
#         assistant_message = f"Error: {e}"

#     # add the assistant's response to the screen
#     with st.chat_message("assistant"):
#         st.markdown(assistant_message)

#         st.session_state.messages.append(AIMessage(assistant_message))