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
# 2. CSS STYLING (المصالحة: الزرار + المربع الشفاف + الخط العريض)
# =========================================================
# تحميل خطوط النصوص + خط الأيقونات
st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)

st.markdown("""
<style>
    /* استيراد الخط العريض */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;700;900&family=Cairo:wght@500;700;900&display=swap');
    
    /* 1. تطبيق الخط العريض على النصوص فقط (تجنب الأيقونات) */
    html, body, p, h1, h2, h3, h4, h5, h6, span, div, button, input, textarea, label {
        font-family: 'Outfit', 'Cairo', sans-serif;
    }
    
    /* فرض السماكة (Bold) على النصوص */
    p, li, span, div { font-weight: 500; } 
    h1, h2, h3, h4, h5, h6, .stButton button { font-weight: 900 !important; }

    /* 2. إصلاح الزرار (إرجاع أيقونة السهم) */
    /* بنقول للمتصفح: أي حاجة جوه زرار القائمة استخدم خط الأيقونات */
    [data-testid="stSidebarCollapsedControl"] i,
    [data-testid="stSidebarCollapsedControl"] span {
        font-family: 'Material Icons' !important;
        font-weight: normal !important;
        font-style: normal;
    }

    /* 3. الخلفية الكاملة */
    .stApp {
        background: linear-gradient(135deg, #9b1c31 0%, #d92d4b 50%, #f09819 100%);
        background-attachment: fixed;
        background-size: cover;
    }

    /* 4. إزالة المربع الأسود السفلي (شفافية تامة) */
    [data-testid="stBottom"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    [data-testid="stBottom"] > div {
        background-color: transparent !important;
    }

    /* 5. مربع الكتابة العائم (Floating Glass) */
    .stChatInputContainer > div {
        background-color: rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 30px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .stChatInputContainer textarea { 
        color: white !important;
        font-weight: 700 !important; /* خط عريض للكتابة */
    }

    /* 6. تنظيف الواجهة */
    header {background: transparent !important;}
    [data-testid="stHeader"] {background: transparent !important; pointer-events: none;} /* يسمح بالضغط على الزرار */
    [data-testid="stSidebarCollapsedControl"] {pointer-events: auto;} /* تفعيل زرار القائمة */
    footer {display: none !important;}
    [data-testid="stDecoration"] {display: none;}

    /* 7. القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* 8. الأزرار الذهبية */
    div.stButton > button {
        background: linear-gradient(92deg, #FFD700 0%, #FF8C00 100%); 
        color: #8B0000 !important; 
        border: none;
        border-radius: 12px;
        padding: 16px 40px;
        font-size: 18px;
        font-weight: 900 !important; /* Bold جداً */
        letter-spacing: 1px;
        text-transform: uppercase;
        width: 100%;
        margin-top: 15px;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.6);
        color: black !important;
    }

    /* 9. خطوات التقدم (Bold & Clean) */
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
    .step-title { font-size: 16px; font-weight: 900 !important; margin: 0; color: #fff !important; }
    .step-active .step-title { color: #FFD700 !important; }
    .step-desc { font-weight: 700 !important; opacity: 0.8; }

    /* 10. الشات */
    .stChatMessage { background: transparent; }
    [data-testid="chatAvatarIcon-assistant"], [data-testid="chatAvatarIcon-user"] { display: none !important; }
    .chat-label { font-size: 14px; font-weight: 900; margin-bottom: 8px; letter-spacing: 1px; text-transform: uppercase; }
    .chat-bubble { padding: 20px; border-radius: 16px; font-size: 18px; font-weight: 600; line-height: 1.6; }

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

if 'page' not in st.session_state: st.session_state.page = 'landing'
if 'phase' not in st.session_state: st.session_state.phase = 1
if 'messages' not in st.session_state: st.session_state.messages = []

def go_to_app():
    st.session_state.page = 'app'
    if not st.session_state.messages:
        st.session_state.messages = [{"role": "assistant", "content": "SYSTEM READY. DESCRIBE YOUR STARTUP IDEA."}]

def reset_app():
    st.session_state.page = 'landing'
    st.session_state.phase = 1
    st.session_state.messages = []

# =========================================================
# 4. الصفحة الرئيسية
# =========================================================
if st.session_state.page == 'landing':
    c1, c2 = st.columns([1,1])
    with c1: st.markdown("<h3>SMART FOUNDER</h3>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    c_txt, c_img = st.columns([5, 4])
    with c_txt:
        st.write("")
        st.markdown('<p style="color:#FFD700 !important; letter-spacing:3px; font-weight:900;">AI-POWERED PARTNER</p>', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 80px; font-weight: 900; line-height: 1;">SMART<br>CO-FOUNDER</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown("<p style='font-weight:700;'>BUILD YOUR STARTUP WITH THE POWER OF AI. VALIDATE IDEAS, PLAN STRATEGIES, AND EXECUTE.</p>", unsafe_allow_html=True)
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
    
    with st.sidebar:
        st.markdown("### CONTROL CENTER")
        st.write("")
        
        steps = [(1, "BRAINSTORMING", "IDEA VALIDATION"), (2, "BLUEPRINT", "STRATEGIC PLAN"), (3, "EXECUTION", "GROWTH TOOLS")]
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
        
        chat_cont = st.container()
        with chat_cont:
            for msg in st.session_state.messages:
                is_ai = msg["role"] == "assistant"
                label = "AI CONSULTANT" if is_ai else "YOU"
                color = "#FFD700" if is_ai else "#FFF"
                bg = "rgba(255,255,255,0.1)" if is_ai else "rgba(0,0,0,0.3)"
                
                st.markdown(f"""
                <div style="margin-bottom: 20px;">
                    <div class="chat-label" style="color:{color} !important;">{label}</div>
                    <div class="chat-bubble" style="background:{bg}; border: 1px solid rgba(255,255,255,0.1);">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.write("<br><br>", unsafe_allow_html=True)

        if prompt := st.chat_input("TYPE HERE..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            with st.spinner("ANALYZING..."):
                full_ctx = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                reply = get_ai_response(f"Act as a professional startup consultant. No emojis. Short and bold answers. Context: {full_ctx}")
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

    elif st.session_state.phase == 2:
        st.markdown("## STRATEGIC BLUEPRINT")
        st.success("PLAN GENERATED SUCCESSFULLY")
        st.markdown("""<div style="background:rgba(0,0,0,0.4); padding:30px; border-radius:15px;"><h3>EXECUTIVE SUMMARY</h3><p>YOUR AI STRATEGY IS READY.</p></div>""", unsafe_allow_html=True)
        if st.button("GO TO EXECUTION"):
            st.session_state.phase = 3
            st.rerun()

    elif st.session_state.phase == 3:
        st.markdown("## EXECUTION TOOLS")
        t1, t2 = st.tabs(["SUPPLIERS", "MARKETING"])
        with t1:
            st.text_input("SEARCH DATABASE")
            st.button("FIND")
        with t2:
            st.button("CREATE CAMPAIGN")
