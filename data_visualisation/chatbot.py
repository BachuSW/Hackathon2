import os
import streamlit as st
import google.generativeai as gen_ai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API key not found. Set GOOGLE_API_KEY in environment variables.")
    st.stop()

# Configure Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-1.5-flash")

# Function to read graph data from training.txt
def get_graph_data():
    try:
        with open("training.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "No training data found."

def chatbot():
    st.title("📊 Gemini Chatbot with Graph Data")

    # Initialize session state variables
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "graph_data" not in st.session_state:
        st.session_state.graph_data = None  # Graph data will be stored here

    # Read training data if not already stored
    if st.session_state.graph_data is None:
        st.session_state.graph_data = get_graph_data()

    # Display chat history
    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(text)

    user_prompt = st.chat_input("Say 'hi' to start...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append(("user", user_prompt))

        # Construct a prompt with graph data prepended
        prompt = f"""
        Here is important data extracted from various graphs:
        {st.session_state.graph_data}

        Based on this information, answer the following question:
        {user_prompt}
        """

        # Send the prompt to Gemini
        response = model.generate_content(prompt)

        # Extract response text safely
        ai_response = getattr(response, "text", "I couldn't process that.")

        with st.chat_message("assistant"):
            st.markdown(ai_response)
        st.session_state.chat_history.append(("assistant", ai_response))