import streamlit as st
import google.generativeai as genai
import time

# ---------------------------------------------------------
# 1. إعدادات الصفحة (لازم تكون أول سطر)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Smart Founder | AI Ultimate",
    layout="wide",
    page_icon="🦅",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. التصميم (Black & Gold Theme) ✨
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Cairo', sans-serif;
    }

    h1, h2, h3, .gold-text {
        color: #D4AF37 !important;
    }

    .stChatMessage {
        background-color: transparent;
        border: none;
        padding: 1rem;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #1A1C24;
        border-radius: 15px;
        border: 1px solid #333;
    }

    div.stButton > button {
        background: transparent;
        border: 1px solid #444;
        color: #eee;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        width: 100%;
        font-weight: 600;
    }
    div.stButton > button:hover {
        border-color: #D4AF37;
        color: #D4AF37;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.1);
    }
    div.stButton > button:active {
        background-color: #D4AF37;
        color: black;
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px;
        border: 1px solid #333;
        background-color: #0E1117;
        color: white;
    }
    .stTextInput input:focus {
        border-color: #D4AF37;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #222;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. المحرك الهجين (Hybrid AI Engine) 🛡️
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome, Founder! 🦅\n\nI'm your AI Partner. Let's discuss your startup idea. What's on your mind?"}
    ]
if "stage" not in st.session_state:
    st.session_state.stage = "chat" 
if "project_data" not in st.session_state:
    st.session_state.project_data = ""

# قائمة الموديلات بالترتيب (لو واحد فشل التاني يشتغل)
MODELS_TO_TRY = [
    "gemini-2.5-flash",        # الأحدث والأسرع
    "gemini-1.5-flash-001",    # النسخة المستقرة (بالاسم الكامل)
    "gemini-pro"               # الاحتياطي القديم
]

def smart_generate(prompt_text):
    """يجرب الموديلات واحد تلو الآخر حتى ينجح"""
    last_error = ""
    
    for model_name in MODELS_TO_TRY:
        try:
            # محاولة استخدام الموديل الحالي
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt_text)
            
        except Exception as e:
            last_error = str(e)
            # لو الخطأ (429) يعني ضغط رسائل، نستنى ونحاول بنفس الموديل مرة كمان
            if "429" in str(e) or "ResourceExhausted" in str(e):
                time.sleep(2)
                try:
                    return model.generate_content(prompt_text)
                except:
                    continue # لو فشل تاني، ننقل للموديل اللي بعده
            
            # لو الخطأ (404) يعني الموديل مش موجود، ننقل للي بعده فوراً
            continue
            
    # لو كل الموديلات فشلت
    st.error(f"⚠️ All AI models are busy currently. Error: {last_error}")
    return None

# 👇👇👇👇 مكان المفتاح (أهم نقطة) 👇👇👇👇
try:
    api_key = "AIzaSyD753gzu6nM_k8jXNkUz0bOQApxIojeZOo"
    genai.configure(api_key=api_key)
except:
    st.warning("⚠️ Please insert your API Key in the code (Line 115).")
    st.stop()

# ---------------------------------------------------------
# 4. القائمة الجانبية (Control Center)
# ---------------------------------------------------------
with st.sidebar:
    st.header("🦅 Smart Founder")
    st.caption("Ultimate Edition v4.0")
    st.write("---")
    
    if st.session_state.stage == "chat":
        st.info("💡 **Phase 1: Brainstorming**")
        st.markdown("Chat to refine your idea.")
        
        if len(st.session_state.messages) > 2:
            st.write("")
            if st.button("🚀 Analyze & Build Plan"):
                with st.spinner("Analyzing your idea..."):
                    history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                    prompt = f"""
                    Summarize this startup discussion into a professional Business Blueprint.
                    Format using Markdown. Include: Project Name, Value Proposition, Target Audience, and 3 Key Next Steps.
                    Conversation:
                    {history}
                    """
                    response = smart_generate(prompt)
                    if response:
                        st.session_state.project_data = response.text
                        st.session_state.stage = "dashboard"
                        st.rerun()
        
        st.write("---")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = [{"role": "assistant", "content": "Let's start fresh! What's your new idea?"}]
            st.rerun()

    elif st.session_state.stage == "dashboard":
        st.success("✅ **Phase 2: Execution**")
        if st.button("⬅️ Back to Brainstorming"):
            st.session_state.stage = "chat"
            st.rerun()

# ---------------------------------------------------------
# 5. واجهة التطبيق (Main Interface)
# ---------------------------------------------------------

# === VIEW 1: CHAT ===
if st.session_state.stage == "chat":
    st.markdown("### 🧠 Brainstorming Room")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Type your idea here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🦅 Thinking...")
            
            full_prompt = f"""
            Act as an expert Startup Consultant. Keep answers concise (max 3 sentences) and conversational.
            Ask one follow-up question to help the user refine their idea.
            
            History: {[m['content'] for m in st.session_state.messages[-4:]]}
            User: {prompt}
            """
            
            response = smart_generate(full_prompt)
            
            if response:
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                message_placeholder.markdown("⚠️ Connection issue. Retrying...")

# === VIEW 2: DASHBOARD ===
elif st.session_state.stage == "dashboard":
    st.markdown("## 🚀 Execution Dashboard")
    
    with st.container():
        st.markdown("""<div style="background:#151515; padding:20px; border-radius:15px; border:1px solid #333;">""", unsafe_allow_html=True)
        st.markdown(st.session_state.project_data)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    
    tab1, tab2 = st.tabs(["🏭 Suppliers Database", "📈 Marketing Engine"])
    
    with tab1:
        st.header("Find Resources")
        c1, c2 = st.columns([3, 1])
        with c1:
            q = st.text_input("Search for (e.g., Packaging, Developers)...")
        with c2:
            st.write("")
            st.write("")
            st.button("Search")
        
        if q:
            st.info(f"Simulating search for: **{q}**")
            st.markdown("""
            * **Supplier A:** Cairo - Verified - 010xxxx
            * **Supplier B:** Giza - Wholesale - 012xxxx
            """)

    with tab2:
        st.header("Content Strategy")
        platform = st.selectbox("Platform", ["TikTok", "Instagram", "LinkedIn"])
        if st.button("⚡ Generate Weekly Plan"):
            with st.spinner("Generating viral ideas..."):
                prompt = f"Create a 3-day content plan for this project on {platform}. Format as a Markdown Table."
                res = smart_generate(prompt)
                if res:
                    st.markdown(res.text)
