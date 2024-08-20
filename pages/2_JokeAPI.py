import streamlit as st  
from style import global_page_style2
import time
import os
from dotenv import load_dotenv
import requests


load_dotenv()


def chat(messages, question):  
    messages.append({"role": "user", "content": "👤: " + question})  
    with st.chat_message("user", avatar="👤"):  
        st.markdown(question)  
    with st.spinner('Processing...'): 
        time.sleep(5) 
        m_strVaultURL = os.environ["vaulturl"] + question
        response = requests.get(m_strVaultURL)  
        if response.status_code == 200:
            data = response.json()
            joke = data.get('response')
            messages.append({"role": "assistant", "content": "🤖: " + joke})  
            with st.chat_message("assistant", avatar="🤖"):  
                st.markdown(joke)  
        else:  
            messages.append({"role": "assistant", "content": "🤖: " + f"Error: {response.status_code} - {response.text}"})  
            with st.chat_message("assistant", avatar="🤖"):  
                st.markdown( f"Error: {response.status_code} - {response.text}")  
  
def clear_session(messages):  
    # Clear necessary session state variables  
    st.cache_data.clear()  
    messages.clear()  
    return messages  
  
def main():  
    st.title("JokeAPI")  
    st.write("-"*50)
    # clear_chat_placeholder = st.empty()  
      
    if 'messages' not in st.session_state:  
        st.session_state.messages = []  
  
    for message in st.session_state.messages:  
        with st.chat_message(message["role"], avatar="✔️"):  
            st.markdown(message['content'])  
    # st.write("-"*50)
    # clear_chat_placeholder = st.empty()  
    # if clear_chat_placeholder.button('Start New Session'):  
    #     st.session_state.messages = clear_session(st.session_state.messages)  
    #     clear_chat_placeholder.empty()  
    #     st.success("JokeAPI session has been reset.")  
    question = st.chat_input('Describe the joke here... ')  
    if question:  
        chat(st.session_state.messages, question)  
        st.write('-'*50)
    clear_chat_placeholder = st.empty()  
    if clear_chat_placeholder.button('Start New Session'):  
        st.session_state.messages = clear_session(st.session_state.messages)  
        clear_chat_placeholder.empty()  
        st.success("JokeAPI session has been reset.")  
  
if __name__ == '__main__':  
    global_page_style2()  
    main()  
