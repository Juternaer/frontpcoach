import streamlit as st
import requests
import random

API_URL = "http://localhost:8000/chat"

##  CHANGE: add one random question to the first prompt, so the llm knows what was asked
INITIAL_QUESTIONS = [
    "Hi there! I'm here to listen. How are you feeling today?",
    "Hello! What would you like to talk about today?",
    "Good day! What's on your mind right now?",
    "Hi! How can I support you today?",
    "How do you feel?",
    "How was your breakfast?",
    "How was your dinner?"
]

st.set_page_config(page_title="Therapist Chat", page_icon="💬")


# if there paramaters available from the chat, initialize
if "session_id" not in st.session_state:
    params = st.query_params
    sid_list = params.get("session_id", [])
    sid = sid_list[0] if sid_list else None
    st.session_state.session_id = sid




## if there is no history or no sessions_state, initialize
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initialized" not in st.session_state:
    # Show a first UX prompt locally    ###(adjust later)
    first_q = random.choice(INITIAL_QUESTIONS)
    st.session_state.messages.append({"role": "assistant", "content": first_q})
    st.session_state.initialized = True

st.title("Therapist Chat")

# Display the chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input area
if user_input := st.chat_input("Your message..."):
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 2. Prepare payload
    payload = {"message": user_input}
    if st.session_state.session_id:
        payload["session_id"] = st.session_state.session_id

    # 3. Send to backend
    with st.spinner("Therapist is thinking..."):
        try:
            resp = requests.post(API_URL, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            # 4. Update session_id (and persist in URL if new)
            new_sid = data.get("session_id", None)
            if new_sid and new_sid != st.session_state.session_id:
                st.session_state.session_id = new_sid
                st.query_params = {"session_id": [new_sid]}

            # 5. Extract assistant reply
            reply = data.get("llm_response", "")
            sentiment = data.get("sentiment")
        except Exception as e:
            st.error(f"Error: {e}")
            reply = "Sorry, I couldn't reach the server."
            sentiment = None

    # Keep for demo purposes, delete later
    if sentiment:
        label = sentiment.get("label", "")
        score = sentiment.get("score", 0.0)
        st.chat_message("assistant").write(f"*Sentiment: {label} ({score:.1%})*")

    # Displaying LLM reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
