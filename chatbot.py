import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)



st.set_page_config(page_title = "Gemini Chatbot",
                   page_icon="👩‍🏫",
                   initial_sidebar_state = "expanded")
st.title = "Gemini Chatbot"

user_query = ""

if "login_status" not in st.session_state or st.session_state["login_status"] == False:
    with st.form("login"):
        st.markdown("## Login 登錄")
        password = st.text_input("**Password 密碼**", type = "password", autocomplete ="password")
        submit = st.form_submit_button()
        
        if submit == True and password.strip() == st.secrets["login"]:
            st.session_state["login_status"] = True
            st.toast('Successfully logged in', icon="✅")
            st.rerun()
            
        else:
            st.session_state["login_status"] = False 
            
            if submit == True and password != st.secrets["login"]: 
                st.write(":red[Wrong password.Please try again]")


if "login_status" in st.session_state and st.session_state["login_status"] == True: 
    # Ensure users have been logged in

    # saving chat memory to streamlit session state, with a key named massages
    msgs = StreamlitChatMessageHistory(key = 'massages')

    # tell langchain how to store memory and pass memory to gpt
    memory = ConversationBufferMemory(memory_key="chat_history",chat_memory=msgs, return_messages=True)

    with st.sidebar:
        prompt = st.text_area("系統提示詞", value = "")
        temperature = st.slider("溫度", 
                                min_value = 0.0,
                                max_value = 1.0,
                                step = 0.1, 
                                value = 0.5)
    
    
    prompt = ChatPromptTemplate.from_template(prompt + "Chat history: {chat_history}\nHuman: {user_question}\nAI:")

    llm = ChatOpenAI(openai_api_key = st.secrets["openai_api"], 
                     model = st.secrets["model"],
                     temperature = temperature,
                     base_url = st.secrets["base_url"]) 

    coversation_chain = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)
    
    avatars = {"human": "user", "ai": "assistant" } # Icon of AI and human

    with st.container():
        container1 = st.container(height = None) # Size varies with the content
        
        user_query = st.chat_input("請輸入……")
        
        if len(msgs.messages) == 0:
            msgs.add_ai_message("Hi, 我有什麼可以幫你的")
            
        for msg in msgs.messages:
                container1.chat_message(avatars[msg.type]).write(msg.content)

        if user_query:
            container1.chat_message("user").write(user_query)
            
            with container1.chat_message("assistant"):
                with st.spinner("生成需時，請耐心等候"):
                    response = coversation_chain.run(user_query)
                    st.write(response)