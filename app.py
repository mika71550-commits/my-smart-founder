import streamlit as st
import google.generativeai as genai
import time

# =========================================================
# 1. إعدادات الصفحة
# =========================================================
st.set_page_config(
    page_title="Smart Co-Founder",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. تحميل مكتبة الأيقونات (الحل الجذري) 🛠️
# =========================================================
st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)

# =========================================================
# 3. CSS Styling (بدون أخطاء)
# =========================================================
st.markdown("""
<style>
    /* استيراد الخطوط */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&family=Cairo:wght@400;700;900&display=swap');
    
    /* 1. تطبيق الخط الجديد على النصوص الصريحة فقط */
    /* شلنا النجمة * عشان منبوظش الدنيا */
    .stApp, div:not(.material-icons), p, h1, h2, h3, h4, h5, h6, span:not(.material-icons), button, input, textarea, label {
        font-family: 'Outfit', 'Cairo', sans-serif !important;
        color: white !important;
    }
    
    /* 2. حماية الأيقونات وإجبارها على الظهور */
    /* ده الكود اللي بيرجع السهم */
    [data-testid="stSidebarCollapsedControl"] i,
    [data-testid="stSidebarCollapsedControl"] span,
    .material-icons {
        font-family: 'Material Icons' !important;
        font-weight: normal;
        font-style: normal;
        font-size: 24px; /* حجم مناسب */
        display: inline-block;
        color: white !important;
    }

    /* 3. الخلفية الكاملة */
    .stApp {
        background: linear-gradient(135deg, #9b1c31 0%, #d92d4b 50%, #f09819 100%);
        background-attachment: fixed;
        background-size: cover;
    }

    /* 4. إزالة المربع الأسود السفلي (شفاف) */
    [data-testid="stBottom"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding-bottom: 20px;
    }
    [data-testid="stBottom"] > div {
        background-color: transparent !important;
    }
    
    /* 5. إخفاء العناصر الزائدة */
    footer {visibility: hidden;}
    [data-testid="stFooter"] {display: none;}
    [data-testid="stHeader"] {background-color: transparent !important;}
    [data-testid="stDecoration"] {display: none;}

    /* 6. مربع الكتابة العائم */
    .stChatInputContainer > div {
        background-color: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 30px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stChatInputContainer textarea { 
        color: white !important;
        font-weight: 700 !important;
    }
    .stChatInputContainer > div:focus-within {
        background-color: rgba(0, 0, 0, 0.6) !important;
        border-color: #FFD700 !important;
    }

    /* 7. القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* 8. الأزرار */
    div.stButton > button {
        background: linear-gradient(92deg, #FFD700 0%, #FF8C00 100%); 
        color: #8B0000 !important; 
        border: none;
        border-radius: 12px;
        padding: 16px 40px;
        font-size: 18px;
        font-weight: 900 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        width: 100%;
        margin-top: 15px;
        font-family: 'Outfit', 'Cairo', sans-serif !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.6);
        color: black !important;
    }

    /* 9. الخطوات */
    .step-box {
        padding: 20px;
        margin-bottom: 12px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid rgba(255, 255, 255, 0.2);
    }
    .step-active {
        background: linear-gradient(90deg, rgba(255, 215, 0, 0.15) 0%, transparent 100%);
        border-left: 5px solid #FFD700;
    }
    .step-title { font-size: 15px; font-weight: 900; margin: 0; color: #fff !important; }
    .step-active .step-title { color: #FFD700 !important; }

    /* 10. الشات */
    .stChatMessage { background: transparent; border: none; padding: 0; margin-bottom: 10px; }
    [data-testid="chatAvatarIcon-assistant"], [data-testid="chatAvatarIcon-user"] { display: none !important; }
    .chat-label { font-size: 13px; font-weight: 900; margin-bottom: 8px; letter-spacing: 1px; text-transform: uppercase; }
    .chat-bubble { padding: 20px; border-radius: 16px; font-size: 18px; font-weight: 600; line-height: 1.6; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }

</style>
""", unsafe_allow_html=True)

# =========================================================
# 4. إعدادات الذكاء الاصطناعي (Gemini 2.5 Flash)
# =========================================================
API_KEY = "AIzaSyC72rNM7BbVuN8mbU9aWet4n2AWrJHEbog" # مفتاحك

# دالة التعامل مع الضغط (Smart Retry)
def get_ai_response(prompt_text):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            genai.configure(api_key=API_KEY)
            # 👇👇 الموديل المطلوب 👇👇
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt_text)
            return response.text
        except Exception as e:
            if "429" in str(e): # لو زحمة
                time.sleep(2) # استنى 2 ثانية
                continue # حاول تاني
            else:
                return f"⚠️ Error: {str(e)}"
    return "⚠️ Server busy. Try again shortly."

if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'phase' not in st.session_state:
    st.session_state.phase = 1
if 'messages' not in st.session_state:
    st.session_state.messages = []

def go_to_app():
    st.session_state.page = 'app'
    if not st.session_state.messages:
        st.session_state.messages = [{"role": "assistant", "content": "Ready to launch. Tell me your idea!"}]

def reset_app():
    st.session_state.page = 'landing'
    st.session_state.phase = 1
    st.session_state.messages = []

# =========================================================
# 5. واجهة الصفحة الرئيسية (Landing)
# =========================================================
if st.session_state.page == 'landing':
    c1, c2 = st.columns([1,1])
    with c1: st.markdown("<h3>SMART FOUNDER</h3>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    col_text, col_img = st.columns([5, 4])
    with col_text:
        st.write("")
        st.markdown('<p style="color:#FFD700 !important; letter-spacing:3px; font-weight:700;">AI-POWERED PARTNER</p>', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 85px; font-weight: 900; line-height: 0.95;">SMART<br>CO-FOUNDER</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        Build your startup with the power of AI. From idea validation to 
        marketing strategies, get everything you need in one unified dashboard.
        """)
        st.write("")
        c_btn, _ = st.columns([2, 1])
        with c_btn:
            if st.button("START JOURNEY 🚀"):
                go_to_app()
                st.rerun()

    with col_img:
        st.image("https://cdni.iconscout.com/illustration/premium/thumb/web-development-2974925-2477356.png", width=650)

# =========================================================
# 6. واجهة التطبيق (App)
# =========================================================
elif st.session_state.page == 'app':
    
    with st.sidebar:
        st.markdown("### CONTROL CENTER")
        st.caption("ID: SESSION-001")
        st.write("")
        
        steps = [
            (1, "BRAINSTORMING", "Idea Validation"),
            (2, "BLUEPRINT", "Strategic Plan"),
            (3, "EXECUTION", "Growth Tools")
        ]
        
        for num, title, desc in steps:
            active_class = "step-active" if st.session_state.phase == num else ""
            st.markdown(f"""
            <div class="step-box {active_class}">
                <p class="step-title">0{num}. {title}</p>
                <p class="step-desc">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("---")
        if st.session_state.phase == 1:
            st.info("💡 Tip: Chat to refine idea, then click Generate.")
            if st.button("GENERATE PLAN"):
                st.session_state.phase = 2
                st.rerun()
        
        st.write("")
        if st.button("EXIT SESSION"):
            reset_app()
            st.rerun()

    # Chat Phase
    if st.session_state.phase == 1:
        st.markdown("## BRAINSTORMING SESSION")
        
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                is_ai = msg["role"] == "assistant"
                bg_color = "rgba(255,255,255,0.15)" if is_ai else "rgba(0,0,0,0.3)"
                label = "AI CONSULTANT" if is_ai else "YOU"
                label_color = "#FFD700" if is_ai else "#FFFFFF"
                
                st.markdown(f"""
                <div style="margin-bottom: 25px;">
                    <div class="chat-label" style="color: {label_color} !important;">{label}</div>
                    <div class="chat-bubble" style="background: {bg_color}; border: 1px solid rgba(255,255,255,0.1);">
                        {msg['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.write("<br><br>", unsafe_allow_html=True)

        if prompt := st.chat_input("Type your idea here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            with st.spinner("Thinking..."):
                full_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                prompt_to_ai = f"Act as a professional startup consultant. Be concise and bold. Context: {full_context}"
                
                ai_reply = get_ai_response(prompt_to_ai)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                st.rerun()

    # Blueprint Phase
    elif st.session_state.phase == 2:
        st.markdown("## STRATEGIC BLUEPRINT")
        st.success("PLAN GENERATED SUCCESSFULLY")
        st.markdown("""
        <div style="background:rgba(0,0,0,0.4); padding:40px; border-radius:15px; border:1px solid rgba(255,255,255,0.2);">
            <h3 style="color:#FFD700 !important;">EXECUTIVE SUMMARY</h3>
            <p style="font-size:20px;"><strong>MISSION:</strong> Dominate the local market with premium quality.</p>
            <br>
            <h3 style="color:#FFD700 !important;">NEXT STEPS</h3>
            <ul>
                <li>STEP 01: Secure Initial Funding</li>
                <li>STEP 02: MVP Development Sprint</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("GO TO EXECUTION"):
            st.session_state.phase = 3
            st.rerun()

    elif st.session_state.phase == 3:
        st.markdown("## EXECUTION TOOLS")
        t1, t2 = st.tabs(["SUPPLIERS", "MARKETING"])
        with t1:
            st.write("")
            st.text_input("SEARCH DATABASE", placeholder="e.g. Packaging...")
            st.button("FIND SUPPLIERS")
        with t2:
            st.write("")
            st.button("GENERATE CAMPAIGN")
