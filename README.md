# STREAMLIT CHATBOT

## Description
Welcome to the Streamlit Chatbot repository. As the name suggests, this chatbot operates using Streamlit, Langchain, and the GROQ API key.

## Instructions
There are three options(tabs) to select in this app,
1. SignUp
2. Login
3. Set API

### 1. SignUp
To utilize this chatbot, the user must first register for an account. This section requires three pieces of information:
* <b>Username</b>
* <b>Password</b>
* <b>GROQ API Key</b>

### 2. Login
Once the user has created an account, they can log in by entering their credentials on the sidebar and checking the login checkbox. If incorrect credentials are provided, an error message will prompt the user to try again. If the provided credentials are correct and a valid API key is provided, the user can access the chatbot without any issues. To start a fresh conversation, users can find a "Clear Cache" button in the sidebar, allowing them to reset the conversation.

### 3. Set API
In this tab, users can update or clear their API key. To clear the API key, users need to provide their username and password and click "Clear API". If the provided credentials are correct, the API key will be removed from the database.

### PROS
1. The data is stored in a database using SQLite3.
2. The passwords are hashed to provide security.
3. API keys can't be hashed because hashing is a one way process.
4. Can freely clear or update API keys.
5. Possible to upgrade the code to include OpenAI or any other LLMs.
6. We can clear the cache using "Clear Cache" button to start a
   fresh conversation.

### CONS
1. No option to reset the password.
2. No option to delete an account.
3. Only way to remove an account is to delete the entire deployed app.
4. There are chances for glitches to arise like the positions of the
   AI messages and User messages can be shifted.
5. No option to delete the individual chat history or the entire
   chat history at all, similar to account issue.

### THOUGHTS
1. Can improve the UI but I believe its not necessary.
2. Possible to integrate RAG or to load
   previous chat history to resume where we left off.

#### Contributors
1. Jagadeesh Akkineni
