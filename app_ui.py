import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEY = os.getenv("NEBIUS_API_KEY") or os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("NEBIUS_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/")
MODEL_NAME = "openai/gpt-oss-120b"

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CodePilot AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED DARK THEME & GLASSMORPHISM STYLING ---
st.markdown("""
    <style>
    /* Dark Deep Space Background Setup */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d1117 0%, #05070a 100%);
        color: #f0f6fc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Glassmorphism Header */
    .header-card {
        background: rgba(13, 17, 23, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px -10px rgba(99, 102, 241, 0.25);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-title {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.5rem;
        letter-spacing: -0.02em;
        margin: 0;
    }

    .header-subtitle {
        color: #8b949e;
        font-size: 1rem;
        margin-top: 0.4rem;
        font-weight: 400;
    }

    .status-badge {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34d399;
        padding: 0.4rem 0.9rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Modern Chat Message Bubbles */
    .stChatMessage {
        border-radius: 16px !important;
        padding: 1.2rem 1.5rem !important;
        margin-bottom: 1.2rem !important;
        background-color: rgba(22, 27, 34, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .stChatMessage:hover {
        border-color: rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-1px);
    }

    /* Style Chat Input Box */
    .stChatInput > div {
        border-radius: 16px !important;
        border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
        background-color: #161b22 !important;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput > div:focus-within {
        border-color: #a855f7 !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4) !important;
    }

    /* Interactive Quick Prompt Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 14px;
        background: rgba(22, 27, 34, 0.8);
        color: #c9d1d9;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 0.85rem 1.1rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.9) 0%, rgba(168, 85, 247, 0.9) 100%);
        color: #ffffff;
        border-color: transparent;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45);
    }

    /* Custom Sleek Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0d1117;
    }
    ::-webkit-scrollbar-thumb {
        background: #21262d;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #30363d;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("## ⚙️ Control Center")
    st.caption("Customize backend execution parameters.")
    st.divider()
    
    st.markdown("### ⚡ Engine Status")
    st.caption(f"**Provider:** `Groq High-Speed API`")
    st.caption(f"**Active Model:** `{MODEL_NAME}`")
    
    st.divider()
    
    st.markdown("### 🎛️ Parameters")
    temperature = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    
    st.divider()
    if st.button("🗑️ Clear Active Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- GLASSMORPHISM APPLICATION HEADER ---
st.markdown(f"""
    <div class="header-card">
        <div>
            <h1 class="header-title">⚡ CodePilot AI</h1>
            <p class="header-subtitle">Next-gen pair programming assistant • High-Speed Inference Engine</p>
        </div>
        <div class="status-badge">
            <span style="height: 8px; width: 8px; background-color: #34d399; border-radius: 50%; display: inline-block;"></span> Active
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- QUICK ASSIST PROMPT CARDS ---
if not st.session_state.messages:
    st.markdown("##### 🚀 Jumpstart your workflow:")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💡 Debug Python Code", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "How do I fix a RecursionError in Python?"})
            st.rerun()

    with col2:
        if st.button("🏗️ FastAPI Architecture", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Explain clean architecture for a FastAPI backend application."})
            st.rerun()

    with col3:
        if st.button("⚡ SQL Query Optimization", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "How do I write an efficient SQL query with indexes?"})
            st.rerun()

    st.write("")

# --- CHAT HISTORY RENDER ---
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- USER INPUT & AI EXECUTION ---
if user_input := st.chat_input("Ask a question, paste code, or request debugging..."):
    # Append User Input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Generate Assistant Response
    with st.chat_message("assistant", avatar="⚡"):
        if not API_KEY or API_KEY.startswith("gsk_your_actual"):
            st.error("❌ API Key missing! Check `NEBIUS_API_KEY` in your `.env` file.")
        else:
            try:
                client = OpenAI(
                    base_url=BASE_URL,
                    api_key=API_KEY
                )

                api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

                with st.spinner("CodePilot is analyzing code..."):
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=api_messages,
                        temperature=temperature
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                    
                    st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:
                st.error(f"Error communicating with AI model: {str(e)}")