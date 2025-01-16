import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Function to initialize the chatbot
def initialize_chatbot():
    # Initialize the LLM (Groq model)
    llm = OpenAI(api_key=api_key, model="chat-groq")

    # Define a conversation chain
    prompt = PromptTemplate(input_variables=["history", "input"], template="""
        The following is a conversation between a user and a helpful chatbot.
        Conversation history:
        {history}
        
        User: {input}
        Chatbot:
    """)

    conversation = ConversationChain(llm=llm, prompt=prompt)
    return conversation

# Streamlit Application
def main():
    st.title("LangChain & Groq Chatbot")
    
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = ""

    # Initialize the chatbot
    chatbot = initialize_chatbot()

    # User input box
    user_input = st.text_input("You:", key="input")

    if user_input:
        # Generate a response
        response = chatbot.run({"history": st.session_state.chat_history, "input": user_input})
        st.session_state.chat_history += f"User: {user_input}\nChatbot: {response}\n"

    # Display chat history
    st.text_area("Conversation History", value=st.session_state.chat_history, height=300)

# Run the app
if __name__ == "__main__":
    main()
