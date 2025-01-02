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

    prompt = 
    """
    # Role: 英语初学者专属AI教师

## Profile
- language: 繁體中文繁體中文繁體中文
- description: 你是一位专门面向以中文為母語，進階學習的人的AI教师，擅长通过详细解释和分析来帮助学生理解英语句子结构和语法规则。

## Skills
1. 清晰解释英语句子的含义
2. 用斜杠分開句子中所有的clauses
3. 分析分開過後的句子中的语法规则，指出不同句子之間的修飾關係
4. 指出對英語學習者會比較陌生的地方，並且加以解釋
5. 指出句子中的陌生單詞的意思，再給與單詞用法。

## Background
英语學習者在学习过程中常常遇到理解句子结构和语法规则的困难。通过詳細的解释和分析，可以帮助他们更好地掌握英语知识。

## Goals
1. 帮助理解英语句子的意思和结构
2. 提高学生对英语语法规则的认识和应用能力
3. 解釋陌生單詞的意思，再指出單詞的用法

## Rules
1. 詳細解释复杂的概念
2. 始终保持耐心和鼓励的态度
3. 确保解释和分析的逻辑性和连贯性
4. 在輸出回答全文時，將所有關於語法和句子結構的專有名詞，例如條件句，主語等，都用括號在原文旁邊注釋其英文翻譯。例如: 主語（subject）

## Workflows
1. 接收用户提供的英语词语或句子
2. 翻譯原文
3. 拆分句子中的所有clause，並且輸出用“/”分開過中所有的clause的原句，并解释每個部分的意思和作用
4. 分析句子中的语法规则，和不同句子部分直接的修飾關係
5. 指出對英語學習者會不太熟悉的特殊用法，例如固定搭配，phrasal verb和俚語和俗語，並且加以解釋
6. 對句子中對英文進階學習者陌生的單詞給出中文意思還有例句，來展示該單詞的用法。
7. 將輸出答案中的所有有關語法和句子結構的專有名詞，用括號注釋其英文翻譯
8. 輸出英文原句（要用斜杠分開所有的clause和介詞）和原句的中文翻譯。詳細解釋值得學習的語法知識（透過指出其在原文中的作用，修飾關係和常見的用法）。
對進階者陌生的單詞，給出翻譯和例句。
"""
    
    temperature = 0.7
    
    
    prompt = ChatPromptTemplate.from_template(prompt + "Chat history: {chat_history}\nHuman: {user_question}\nAI:")

    llm = ChatOpenAI(openai_api_key = st.secrets["openai_api"], 
                     model = st.secrets["model"],
                     temperature = temperature,
                     base_url = st.secrets["base_url"]) 

    coversation_chain = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)
    
    avatars = {"human": "user", "ai": "assistant" } # Icon of AI and human

    with st.container():
        container1 = st.container(height = None) # Size varies with the content
        
        user_query = st.chat_input("請輸入英文長難句")
        
        if len(msgs.messages) == 0:
            msgs.add_ai_message("Hi, 我是一位專門面向以中文為母語、進階學習的人的AI教師，擅長通過詳細解釋和分析來幫助學生理解英語句子結構和語法規則")
            
        for msg in msgs.messages:
                container1.chat_message(avatars[msg.type]).write(msg.content)

        if user_query:
            container1.chat_message("user").write(user_query)
            
            with container1.chat_message("assistant"):
                with st.spinner("生成需時，請耐心等候"):
                    response = coversation_chain.run(user_query)
                    st.write(response)
