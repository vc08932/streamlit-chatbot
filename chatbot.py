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
st.title = "Your English Sentence Analyst"

user_query = ""
st.session_state["login_status"] = True # Disabled the login function

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

    prompt = """
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
    with st.sidebar:
        user_query = st.chat_input("請輸入……")   
        if user_query:
            st.markdown(user_query)
        
    prompt = ChatPromptTemplate.from_template(prompt + "Chat history: {chat_history}\nHuman: {user_question}\nAI:")

    llm = ChatOpenAI(openai_api_key = st.secrets["openai_api"], 
                     model = st.secrets["model"],
                     temperature = temperature,
                     base_url = st.secrets["base_url"]) 

    coversation_chain = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)
    
    avatars = {"human": "user", "ai": "assistant" } # Icon of AI and human

    with st.container():
        container1 = st.container(height = None) # Size varies with the content
        
        #user_query = st.chat_input("請輸入英文長難句")
        
        if len(msgs.messages) == 0:
            msgs.add_ai_message("""
英語句子分析聊天機器人來啦😎！這款專為以中文為母語的英語進階學習者設計的工具，猶如一位隨時在線的私人英語老師👩‍🏫，功能強大又實用。

它的主要功能包括：首先，能將你輸入的英語句子精準翻譯成中文，讓你迅速掌握句子大意；接著，會用斜杠（`/`）把句子中的所有從句清晰拆分開來，並詳細解釋每部分的意思和作用，幫助你輕鬆把握句子結構；還會深入分析句子的語法規則，指出不同部分之間的修飾關係，加深你對英語語法的理解；對於英語學習者較陌生的特殊用法，如固定搭配、短語動詞和俚語俗語等，也會一一識別並解釋；另外，遇到句子中對英文進階學習者來說陌生的單詞，它會給出中文意思和例句，方便你掌握單詞用法。

使用方法也非常簡單：在輸入框輸入想要分析的英語句子，稍作等待，就能快速獲得詳細的分析結果。有了它，你的英語學習之路將更加輕鬆高效✍️！ 
""")
            
        for msg in msgs.messages:
                container1.chat_message(avatars[msg.type]).write(msg.content)

        if user_query:
            container1.chat_message("user").write(user_query)
            
            with container1.chat_message("assistant"):
                with st.spinner("生成需時，請耐心等候"):
                    response = coversation_chain.run(user_query)
                    st.write(response)
