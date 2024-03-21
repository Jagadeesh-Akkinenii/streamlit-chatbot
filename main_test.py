import sqlite3 
import hashlib
import streamlit as st
from streamlit_chat import message
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os

# DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Security Functions
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT, api_key STRING)')

def add_userdata(username, password, api_key):
	c.execute('INSERT INTO userstable(username,password,api_key) VALUES (?,?,?)',(username,password,api_key))
	conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data

def update_k(username, password, api_key):
     c.execute('UPDATE userstable SET api_key = ? WHERE username =? AND password = ?',(api_key, username, password))
     conn.commit()

def clear_session():
    st.session_state.clear()

def save_chat_history(username, messages):
    # Create a folder if it doesn't exist
    if not os.path.exists('history'):
        os.makedirs('history')
    # Write chat history to a file
    with open(f'history/{username}_chat_history.txt', 'a+') as file:
        for msg in messages:
            file.write(msg.content + '\n')

def save_chat_history(username, messages):
    # Create a folder if it doesn't exist
    if not os.path.exists('history'):
        os.makedirs('history')
    # Write chat history to a file
    with open(f'history/{username}_chat_history.txt', 'a+') as file:
        for msg in messages:
            file.write(msg.content + '\n')

def init():
    st.set_page_config(
        page_title="Your own ChatGPT",
        page_icon="🤖"
    )

def main():
    init()

    menu = ["Login", "SignUp", "Set API"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Login":
        st.cache_resource.clear()
        st.sidebar.title("LOGIN")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        
        if st.sidebar.checkbox("Login"):
            create_usertable()
            
            result = login_user(username, make_hashes(password))

            if result:
                st.sidebar.success("Logged In as {}".format(username))
                try:
                    os.environ["GROQ_API_KEY"] = result[0][2]
                except:
                    st.error("Please give a valid API KEY")
                    st.stop()

                chat = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")

                if "messages" not in st.session_state:
                    st.session_state.messages = [
                        SystemMessage(content="You are a helpful assistant.")
                    ]

                if st.sidebar.button("Clear Cache"):
                    clear_session()

                st.header("Your own ChatGPT 🤖")

                user_input = st.chat_input("Your message:", key="user_input")

                if user_input:
                    st.session_state.messages.append(HumanMessage(content=user_input))

                    with st.spinner("Thinking...."):
                        response = chat(st.session_state.messages)

                    st.session_state.messages.append(AIMessage(content=response.content))

                    with open("indi_chat.txt", "a+") as file:
                        file.write(f"User: {str(user_input)}\n")
                        file.write(f"AI: {str(response.content)}\n")

                    save_chat_history(username, st.session_state.messages)  # Save chat history

                messages = st.session_state.get('messages', [])
                for i, msg in enumerate(messages[1:]):
                    if i % 2 == 0:
                        message(msg.content, is_user=True, key=str(i) + '_user')
                    else:
                        message(msg.content, is_user=False, key=str(i) + '_ai')
            
            else:
                 st.error("Invalid credentials, please re-enter correct login details.")

            
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        new_api_key = st.text_input("API KEY", type = 'password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password),new_api_key)
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
    
    elif choice == "Set API":
        st.subheader("SET OR DELETE API")
        existing_user = st.text_input("Username")
        existing_password = st.text_input("Password",type='password')
        existing_api_key = st.text_input("API KEY", type = 'password')

        if st.button("Update"):
            update_k(existing_user, make_hashes(existing_password), existing_api_key)
            st.success("UPDATED")
            st.info("Go to Login Menu to login")
        if st.button("Clear API"):
            to_clear_api = None
            update_k(existing_user, make_hashes(existing_password), to_clear_api)
                    
if __name__ == '__main__':
    main()
