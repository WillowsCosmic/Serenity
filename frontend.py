import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🌸 Serenity - AI Mental Health therapist 🌸")
st.markdown(""""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app background */
    /* Cute pastel background */
    .stApp {
        background: linear-gradient(135deg, 
            #fff7ed 0%,     /* soft peach */
            #fef3c7 15%,    /* light yellow */
            #ecfdf5 30%,    /* mint green */
            #f0f9ff 45%,    /* sky blue */
            #fdf4ff 60%,    /* lavender */
            #fce7f3 75%,    /* soft pink */
            #fff1f2 90%,    /* rose white */
            #fdf2f8 100%);  /* pink blush */
        font-family: 'Inter', sans-serif;
        animation: gradientShift 10s ease infinite;
    }
    
    /* Cute gradient animation */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Clean title styling */
     h1 {
    color: #0284c7 !important;        /* Soft purple */
    font-weight: 600 !important;
    text-align: center !important;
    margin: 2rem 0 !important;
    font-size: 2.5rem !important;
    text-shadow: 0 2px 8px rgba(124, 58, 237, 0.2) !important;
    # background: linear-gradient(45deg, #7c3aed, #a855f7, #ec4899);
    # -webkit-background-clip: text !important;
    # -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
    
    /* Chat message containers */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(236, 72, 153, 0.2) !important;
        border-radius: 15px !important;
        margin: 1rem 0 !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.1) !important;
    }
    
    /* User messages (right side) */
    div[data-testid="chatAvatarIcon-user"] + div {
        background: linear-gradient(135deg, #ec4899, #be185d) !important;
        color: white !important;
        border: none !important;
    }
            
    
    /* Assistant messages (left side) */
    div[data-testid="chatAvatarIcon-assistant"] + div {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #831843 !important;
        border: 1px solid rgba(236, 72, 153, 0.2) !important;
    }
    
    /* Chat Input Styling - Clean approach */
    .stChatInput,
    div[data-testid="stChatInput"],
    section[data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(236, 72, 153, 0.3) !important;
        border-radius: 25px !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.15) !important;
    }
    
    /* Input text */
    .stChatInput input,
    div[data-testid="stChatInput"] input {
        background: transparent !important;
        color: #831843 !important;
        border: none !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
    }
    
    /* Placeholder */
    .stChatInput input::placeholder,
    div[data-testid="stChatInput"] input::placeholder {
        color: rgba(131, 24, 67, 0.5) !important;
        font-style: italic !important;
    }
    
    /* Send button */
    .stChatInput button,
    div[data-testid="stChatInput"] button {
        background: #ec4899 !important;
        border: none !important;
        border-radius: 50% !important;
        color: white !important;
    }
    
    .stChatInput button:hover,
    div[data-testid="stChatInput"] button:hover {
        background: #be185d !important;
        transform: scale(1.05) !important;
    }
    
    /* Clean main container */
    .main .block-container {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        max-width: 900px !important;
        padding: 2rem 1rem !important;
    }
    
    
    
    /* Clean sidebar */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
            <style>
    /* Chat message text color fixes */
    .stChatMessage p,
    .stChatMessage div,
    .stChatMessage span,
    div[data-testid="chatAvatarIcon-user"] + div p,
    div[data-testid="chatAvatarIcon-user"] + div div,
    div[data-testid="chatAvatarIcon-user"] + div span,
    div[data-testid="chatAvatarIcon-assistant"] + div p,
    div[data-testid="chatAvatarIcon-assistant"] + div div,
    div[data-testid="chatAvatarIcon-assistant"] + div span {
        color: #831843 !important;
        font-weight: 500 !important;
    }
    
    /* User message text should be white */
    div[data-testid="chatAvatarIcon-user"] + div p,
    div[data-testid="chatAvatarIcon-user"] + div div,
    div[data-testid="chatAvatarIcon-user"] + div span {
        color: white !important;
        font-weight: 500 !important;
    }
    
    /* Assistant message text should be dark pink */
    div[data-testid="chatAvatarIcon-assistant"] + div p,
    div[data-testid="chatAvatarIcon-assistant"] + div div,
    div[data-testid="chatAvatarIcon-assistant"] + div span {
        color: #831843 !important;
        font-weight: 500 !important;
    }
    
    /* Force text color override for all chat content */
    .stChatMessage * {
        color: inherit !important;
    }
    
    /* Specific targeting for message content */
    div[class*="stChatMessage"] p {
        color: #831843 !important;
    }
    
    /* User message background and text */
    div[data-testid="chatAvatarIcon-user"] + div {
        background: linear-gradient(135deg, #ec4899, #be185d) !important;
        color: white !important;
        border-radius: 20px 20px 5px 20px !important;
        padding: 1rem 1.5rem !important;
        margin-left: 2rem !important;
    }
    
    div[data-testid="chatAvatarIcon-user"] + div * {
        color: white !important;
    }
    
    /* Assistant message background and text */
    div[data-testid="chatAvatarIcon-assistant"] + div {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #831843 !important;
        border-radius: 20px 20px 20px 5px !important;
        padding: 1rem 1.5rem !important;
        margin-right: 2rem !important;
        border: 1px solid rgba(236, 72, 153, 0.3) !important;
    }
    
    div[data-testid="chatAvatarIcon-assistant"] + div * {
        color: #831843 !important;
    }
            .stChatInput,
div[data-testid="stChatInput"],
section[data-testid="stChatInput"] {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(252, 231, 243, 0.8)) !important;
    border: 2px solid rgba(236, 72, 153, 0.3) !important;
    border-radius: 25px !important;
    backdrop-filter: blur(10px) !important;
}

/* Input text color */
.stChatInput input,
div[data-testid="stChatInput"] input {
    color: #831843 !important;
    background: transparent !important;
}

/* Placeholder text */
.stChatInput input::placeholder,
div[data-testid="stChatInput"] input::placeholder {
    color: rgba(131, 24, 67, 0.6) !important;
}
</style>
""", unsafe_allow_html=True)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Whats on your mind today?")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Get response from backend
    backend_response = requests.post(BACKEND_URL, json={"message": user_input})
    
    # Extract just the therapeutic message from JSON
    response_json = backend_response.json()
    clean_message = response_json.get("response", "I'm here to support you. How can I help?")
    
    st.session_state.chat_history.append({"role": "assistant", "content": clean_message})

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])