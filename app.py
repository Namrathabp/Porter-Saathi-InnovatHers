import streamlit as st
import time
from ai_engine import ask_ai
from voice_client import listen, speak
import pyttsx3


def build_prompt(mode, query):
    if mode == "🤖 General":
        return f"You are Porter Saathi, a friendly AI assistant for truck drivers. Answer simply in Hindi-English mix. Query: {query}"
    
    elif mode == "📊 Finance":
        return f"You are Saathi, a finance buddy for drivers. Always explain in simple terms like earnings after expenses, penalties, rewards. Be short and clear. Query: {query}"
    
    elif mode == "📚 Learning":
        return f"You are Saathi, a patient teacher for drivers with low literacy. Break things into small steps. Use simple Hindi-English and give 1-2 practical examples. Query: {query}"
    
    elif mode == "🚨 Safety":
        return f"You are Saathi, an emergency safety assistant. Speak calmly but urgently. Give direct step-by-step instructions, no extra words. Query: {query}"
    
    else:
        return query

# -------------------------------
# Streamlit Config
# -------------------------------
st.set_page_config(page_title="Porter Saathi", page_icon="🚚", layout="wide")

# -------------------------------
# Sidebar Settings
# -------------------------------
st.sidebar.title("⚙ Settings")
use_tts = st.sidebar.checkbox("Enable Voice Output", value=True)
assistant_mode = st.sidebar.radio("Assistant Mode", ["🤖 General", "📊 Finance", "📚 Learning", "🚨 Safety"])
st.sidebar.markdown("---")
st.sidebar.info("🔑 API Key set in ai_engine.py")

# -------------------------------
# Header
# -------------------------------
st.markdown(
    """
    <div style="text-align: center;">
        <h1>🚚 Porter Saathi</h1>
        <h3>🌏 Voice-First AI Partner for Drivers</h3>
        <p style="color: grey;">Empowering drivers with conversations, not text.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# Conversation State
# -------------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []
if "assistant_thinking" not in st.session_state:
    st.session_state["assistant_thinking"] = False

def add_to_history(role, content):
    st.session_state["history"].append({"role": role, "content": content})
    if len(st.session_state["history"]) > 6:
        st.session_state["history"].pop(0)

# -------------------------------
# Saathi Thinking Indicator
# -------------------------------
def show_thinking():
    placeholder = st.empty()
    with placeholder:
        st.markdown("<i>🤔 Saathi is thinking...</i>", unsafe_allow_html=True)
    time.sleep(1.2)
    placeholder.empty()

# -------------------------------
# Two Column Layout
# -------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎤 Voice Input")
    mic_btn = st.button("🎙 Tap to Speak", use_container_width=True)
    if mic_btn:
        query = listen()
        if query:
            add_to_history("user", query)
            st.write(f"🗣 You said: *{query}*")

            show_thinking()
            prompt = build_prompt(assistant_mode, query)
            ans = ask_ai(prompt)
            add_to_history("saathi", ans)

            st.markdown(f"<div style='padding:10px;border-radius:10px;background:#e6f7ff'><b>🤖 Saathi:</b> {ans}</div>", unsafe_allow_html=True)
            if use_tts:
                speak(ans)

with col2:
    st.subheader("⌨ Text Input")
    manual_query = st.text_input("Type your query:")
    if st.button("💬 Ask", use_container_width=True):
        if manual_query.strip():
            add_to_history("user", manual_query)

            show_thinking()
            prompt = build_prompt(assistant_mode, query)
            ans = ask_ai(prompt)
            add_to_history("saathi", ans)

            st.markdown(f"<div style='padding:10px;border-radius:10px;background:#f6ffed'><b>🤖 Saathi:</b> {ans}</div>", unsafe_allow_html=True)
            if use_tts:
                speak(ans)

# -------------------------------
# Conversation History
# -------------------------------
st.markdown("---")
st.subheader("📝 Conversation History")

for h in st.session_state["history"]:
    if h["role"] == "user":
        st.markdown(f"<div style='padding:8px;border-radius:8px;background:#fffbe6'><b>👤 You:</b> {h['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='padding:8px;border-radius:8px;background:#e6f7ff'><b>🤖 Saathi:</b> {h['content']}</div>", unsafe_allow_html=True)

# -------------------------------
# Emergency Shortcuts
# -------------------------------
st.markdown("---")
st.subheader("🛟 Emergency Help")

with st.container():
    st.error("🚨 Quick Safety Actions")
    colA, colB, colC = st.columns(3)
    with colA:
        if st.button("📞 Call Helpline", use_container_width=True):
            msg = "Connecting you to emergency helpline..."
            add_to_history("saathi", msg)
            st.warning(msg)
            if use_tts: speak(msg)
    with colB:
        if st.button("📍 Share Location", use_container_width=True):
            msg = "Location shared with safety contacts."
            add_to_history("saathi", msg)
            st.warning(msg)
            if use_tts: speak(msg)
    with colC:
        if st.button("💬 Live Agent", use_container_width=True):
            msg = "Connecting you with a live agent..."
            add_to_history("saathi", msg)
            st.warning(msg)
            if use_tts: speak(msg)

# -------------------------------
# Proactive Suggestions
# -------------------------------
st.markdown("---")
st.subheader("✨ Saathi Suggestions")
if assistant_mode == "📊 Finance":
    st.info("💡 Tip: Ask “Aaj ka kharcha kaat ke kitna kamaya?”")
elif assistant_mode == "📚 Learning":
    st.info("💡 Tip: Say “Mujhe vehicle insurance samjhao”")
elif assistant_mode == "🚨 Safety":
    st.info("💡 Tip: Try “Meri gadi kharab ho gayi, kya karu?”")
else:
    st.info("💡 Tip: You can ask anything like “Kal ka kaam behtar tha ya aaj ka?”")

# -------------------------------
# Footer
# -------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🌟 Agentic Prototype — Saathi adapts, suggests, and safeguards. © 2025 Porter")