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
# 2. CSS STYLING (الحل النووي لإخفاء الكلمة) ☢️
# =========================================================
st.markdown("""
<style>
    /* استيراد خط النصوص */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&family=Cairo:wght@400;700;900&display=swap');
    
    /* تطبيق الخط على النصوص العادية */
    html, body, [class*="css"] {
        font-family: 'Outfit', 'Cairo', sans-serif;
    }

    /* === 1. القضاء على كلمة keyboard_double_arrow_right === */
    /* استهداف الزرار اللي بيطلع الكلمة */
    [data-testid="stSidebarCollapsedControl"] {
        color: transparent !important; /* خلي الكلام شفاف (يختفي) */
    }
    
    /* رسم أيقونة بديلة فوق الكلمة المختفية */
    [data-testid="stSidebarCollapsedControl"]::after {
        content: "☰"; /* رمز القائمة العادي (موجود في كل الاجهزة) */
        color: #FFD700; /* لون ذهبي */
        font-size: 30px;
        font-weight: bold;
        position: absolute;
        top: 0;
        left: 0;
        background: rgba(0,0,0,0.3); /* خلفية بسيطة */
        padding: 5px 10px;
        border-radius: 8px;
    }

    /* === 2. الخلفية الكاملة === */
    .stApp {
        background: linear-gradient(135deg, #9b1c31 0%, #d92d4b 50%, #f09819 100%);
        background-attachment: fixed;
        background-size: cover;
    }

    /* === 3. تنظيف الواجهة === */
    /* إخفاء الهيدر والفوتر */
    header {background: transparent !important;}
    [data-testid="stHeader"] {background: transparent !important; z-index: 999;}
    [data-testid="stDecoration"] {display: none;}
    footer {display: none !important;}
    
    /* إخفاء الشريط السفلي (المربع الأسود) */
    [data-testid="stBottom"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* === 4. تصميم مربع الكتابة === */
    .stChatInputContainer > div {
        background-color: rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 30px !important;
        color: white !important;
    }
    .stChatInputContainer textarea {
        color: white !important;
        font-weight: 700 !important;
        caret-color: #FFD700;
    }

    /* === 5. القائمة الجانبية === */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.1);
        padding-top: 20px;
    }
    
    /* تلوين نصوص القائمة */
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: white !important;
    }

    /* === 6. الأزرار === */
    div.stButton > button {
        background: linear-gradient(92deg, #FFD700 0%, #FF8C00 100%); 
        color: #8B0000 !important; 
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: 900 !important;
        text-transform: uppercase;
        width: 100%;
        margin-top: 10px;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }

    /* === 7. الفقاعات والخطوات === */
    .step-box {
        padding: 15px; margin-bottom: 10px; border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid rgba(255, 255, 255, 0.2);
    }
    .step-active {
        background: linear-gradient(90deg, rgba(255, 215, 0, 0.15) 0%, transparent 100%);
        border-left: 4px solid #FFD700;
    }
    .step-title { font-weight: 900; margin: 0; color: white !important; }
    .step-active .step-title { color: #FFD700 !important; }

    /* الشات */
    .stChatMessage { background: transparent; }
    [data-testid="chatAvatarIcon-assistant"], [data-testid="chatAvatarIcon-user"] { display: none !important; }

</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. إعدادات الذكاء (Gemini 2.5 Flash)
# =========================================================
API_KEY = "AIzaSyC72rNM7BbVuN8mbU9aWet4n2AWrJHEbog"

def get_ai_response(prompt_text):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt_text)
            return response.text
        except Exception as e:
            if "429" in str(e):
                time.sleep(2)
                continue
            return f"⚠️ Error: {str(e)}"
    return "⚠️ Server busy. Please try again."

# State Management
if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'phase' not in st.session_state: st.session_state.phase = 1
if 'messages' not in st.session_state: st.session_state.messages = []

# Navigation Functions
def go_to_app():
    st.session_state.page = 'app'
    if not st.session_state.messages:
        st.session_state.messages = [{"role": "assistant", "content": "Ready. Tell me your idea!"}]

def reset_app():
    st.session_state.page = 'landing'
    st.session_state.phase = 1
    st.session_state.messages = []

# =========================================================
# 4. الصفحة الرئيسية
# =========================================================
if st.session_state.page == 'landing':
    col1, col2 = st.columns([1,1])
    with col1: st.markdown("<h3>SMART FOUNDER</h3>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    c_txt, c_img = st.columns([5, 4])
    with c_txt:
        st.write("")
        st.markdown('<p style="color:#FFD700; letter-spacing:3px; font-weight:700;">AI-POWERED PARTNER</p>', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 80px; font-weight: 900; line-height: 1;">SMART<br>CO-FOUNDER</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown("Build your startup with the power of AI.")
        st.write("")
        
        btn_col, _ = st.columns([2, 1])
        with btn_col:
            if st.button("START JOURNEY 🚀"):
                go_to_app()
                st.rerun()

    with c_img:
        st.image("https://cdni.iconscout.com/illustration/premium/thumb/web-development-2974925-2477356.png", width=650)

# =========================================================
# 5. واجهة التطبيق
# =========================================================
elif st.session_state.page == 'app':
    
    # Sidebar
    with st.sidebar:
        st.markdown("### CONTROL CENTER")
        st.write("")
        
        steps = [(1, "BRAINSTORMING", "Idea Validation"), (2, "BLUEPRINT", "Strategic Plan"), (3, "EXECUTION", "Growth Tools")]
        for num, title, desc in steps:
            active = "step-active" if st.session_state.phase == num else ""
            st.markdown(f"""<div class="step-box {active}"><p class="step-title">0{num}. {title}</p><p class="step-desc">{desc}</p></div>""", unsafe_allow_html=True)
        
        st.write("---")
        if st.session_state.phase == 1:
            if st.button("GENERATE PLAN"):
                st.session_state.phase = 2
                st.rerun()
        
        st.write("")
        if st.button("EXIT SESSION"):
            reset_app()
            st.rerun()

    # Content
    if st.session_state.phase == 1:
        st.markdown("## BRAINSTORMING SESSION")
        
        # Chat Messages
        chat_cont = st.container()
        with chat_cont:
            for msg in st.session_state.messages:
                is_ai = msg["role"] == "assistant"
                label = "AI CONSULTANT" if is_ai else "YOU"
                color = "#FFD700" if is_ai else "#FFF"
                bg = "rgba(255,255,255,0.15)" if is_ai else "rgba(0,0,0,0.3)"
                
                st.markdown(f"""
                <div style="margin-bottom: 20px;">
                    <div style="color:{color}; font-weight:bold; font-size:12px; margin-bottom:5px;">{label}</div>
                    <div style="background:{bg}; padding:15px; border-radius:15px;">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.write("<br><br>", unsafe_allow_html=True)

        # Input
        if prompt := st.chat_input("Type here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

        # Response
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            with st.spinner("Analyzing..."):
                full_ctx = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                reply = get_ai_response(f"Act as a pro consultant. Concise. Context: {full_ctx}")
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

    elif st.session_state.phase == 2:
        st.markdown("## STRATEGIC BLUEPRINT")
        st.success("PLAN GENERATED")
        st.markdown("""<div style="background:rgba(0,0,0,0.4); padding:30px; border-radius:15px;"><h3>EXECUTIVE SUMMARY</h3><p>Your AI Plan is ready.</p></div>""", unsafe_allow_html=True)
        if st.button("GO TO EXECUTION"):
            st.session_state.phase = 3
            st.rerun()

    elif st.session_state.phase == 3:
        st.markdown("## EXECUTION TOOLS")
        t1, t2 = st.tabs(["SUPPLIERS", "MARKETING"])
        with t1:
            st.text_input("SEARCH")
            st.button("FIND")
        with t2:
            st.button("CREATE CAMPAIGN")
