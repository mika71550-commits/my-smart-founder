iimport streamlit as st
import google.generativeai as genai
import time

# ---------------------------------------------------------
# 1. إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="Smart Co-Founder",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. تحويل التصميم لكود (CSS Magic) 🎨
# ---------------------------------------------------------
# هنا بنرسم الخلفية المتدرجة (Gradient) وبنغير الخطوط
st.markdown("""
<style>
    /* استيراد خط Montserrat عشان يبقى شبه الصورة */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;700;900&family=Cairo:wght@400;700&display=swap');

    /* 1. الخلفية المتدرجة (Red/Orange Gradient) */
    .stApp {
        background: #8E2DE2;  /* fallback for old browsers */
        background: -webkit-linear-gradient(to right, #4A00E0, #8E2DE2);  /* Chrome 10-25, Safari 5.1-6 */
        background: linear-gradient(135deg, #9b1c31 0%, #d92d4b 50%, #f09819 100%); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    }

    /* 2. النصوص بيضاء */
    h1, h2, h3, h4, p, div, span {
        color: white !important;
        font-family: 'Montserrat', 'Cairo', sans-serif;
    }

    /* 3. إخفاء الهيدر الافتراضي بتاع Streamlit */
    header {visibility: hidden;}
    
    /* 4. تنسيق الزرار (Call to Action) */
    div.stButton > button {
        background: linear-gradient(90deg, #F09819 0%, #EDDE5D 100%);
        color: #9b1c31 !important; /* لون النص نبيتي */
        border: none;
        border-radius: 30px; /* حواف دائرية */
        padding: 15px 40px;
        font-size: 20px;
        font-weight: 900;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        color: black !important;
    }

    /* 5. الناف بار (Simulation) */
    .navbar {
        display: flex;
        justify-content: flex-end;
        gap: 30px;
        padding: 20px;
        font-weight: bold;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* 6. النصوص الكبيرة */
    .big-title {
        font-size: 80px;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    .sub-title {
        font-size: 24px;
        font-weight: 300;
        letter-spacing: 2px;
        margin-bottom: 30px;
        opacity: 0.9;
    }
    .desc {
        font-size: 16px;
        line-height: 1.6;
        opacity: 0.8;
        max-width: 500px;
        margin-bottom: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. إدارة الحالة (عشان ننتقل من اللاندنج للأبليكشن)
# ---------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'landing' # landing OR app

def go_to_app():
    st.session_state.page = 'app'

# ---------------------------------------------------------
# 4. محتوى الصفحة (Landing Page View)
# ---------------------------------------------------------
if st.session_state.page == 'landing':
    
    # 1. Navbar (HTML)
    st.markdown("""
    <div class="navbar">
        <span>Home</span>
        <span>About Us</span>
        <span>Services</span>
        <span>Contact</span>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # 2. Main Hero Section (Layout 50/50)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("") # Spacer
        st.write("") 
        
        # النصوص بتنسيق HTML عشان نتحكم في الحجم بالظبط زي الصورة
        st.markdown('<div class="sub-title">AI-POWERED STARTUP PARTNER</div>', unsafe_allow_html=True)
        st.markdown('<div class="big-title">SMART<br>CO-FOUNDER</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="desc">
        حول فكرتك إلى مشروع ناجح باستخدام أحدث تقنيات الذكاء الاصطناعي.
        احصل على خطط عمل، استراتيجيات تسويق، وقاعدة بيانات موردين، كل ذلك في مكان واحد وبضغطة زر.
        </div>
        """, unsafe_allow_html=True)
        
        # زرار البداية
        if st.button("🚀 ABDA' REHLETAK | ابدأ رحلتك"):
            go_to_app()
            st.rerun()

    with col2:
        # صورة اللابتوب (جبتلك صورة 3D قريبة جداً من اللي في التصميم خلفيتها شفافة)
        st.image("https://cdni.iconscout.com/illustration/premium/thumb/web-development-2974925-2477356.png", width=600)

# ---------------------------------------------------------
# 5. محتوى التطبيق (App View) - لما يضغط ابدأ
# ---------------------------------------------------------
elif st.session_state.page == 'app':
    
    # نرجع الخلفية سوداء عشان التطبيق يبقى مريح للعين وقت الشغل
    st.markdown("""
    <style>
    .stApp {
        background: #0E1117; /* Dark Mode for App */
    }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # هنا كود التطبيق الأساسي (Chat & Logic)
    # -----------------------------------------------------
    
    # 👇👇 حط مفتاحك هنا 👇👇
    try:
        api_key = "AIzaSyD753gzu6nM_k8jXNkUz0bOQApxIojeZOo" # ضع مفتاحك هنا
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        st.warning("⚠️ Please configure API Key.")

    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=50)
        st.header("Smart Tools")
        if st.button("⬅️ Back to Home"):
            st.session_state.page = 'landing'
            st.rerun()

    # Chat UI
    st.title("🦅 Smart Co-Founder Dashboard")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome aboard! What idea are we building today?"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Tell me your idea..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Simple AI Call
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.write(response.text)
        except:
            st.error("AI connection error.")
