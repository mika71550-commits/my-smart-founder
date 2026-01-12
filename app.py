import streamlit as st
import pandas as pd
import google.generativeai as genai

# ---------------------------------------------------------
# 1. إعدادات المخ (Gemini)
# ---------------------------------------------------------
# مفتاحك الشغال
api_key = "AIzaSyApXN9pIUqM-k4DzDuNtRHPERpOoA7ph8g" 
genai.configure(api_key=api_key)

# التعديل المهم جداً: استخدمنا الموديل اللي ظهر عندك في الفحص
model = genai.GenerativeModel('gemini-2.5-flash')

# ---------------------------------------------------------
# 2. تحميل الداتا (للقسم الأول)
# ---------------------------------------------------------
try:
    df = pd.read_csv("data.csv")
except:
    df = pd.DataFrame(columns=["category", "name", "location", "details", "contact"])

# ---------------------------------------------------------
# 3. واجهة التطبيق الرئيسية
# ---------------------------------------------------------
st.set_page_config(page_title="المؤسس الذكي", layout="wide", page_icon="🚀")

st.title("🚀 Smart Co-Founder | شريكك الذكي")
st.markdown("---")

tab1, tab2 = st.tabs(["🏭 التنفيذ والموردين", "📈 التسويق والنمو"])

# =========================================================
# التبويب الأول: التنفيذ والموردين
# =========================================================
with tab1:
    st.header("دليل التنفيذ والموردين")
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("بحث عن مورد (مثلاً: بن، تغليف، ملابس)...", key="supplier_search")
    
    if search_query:
        found = False
        for index, row in df.iterrows():
            row_str = f"{row['category']} {row['name']} {row['details']}"
            if search_query in row_str:
                with st.expander(f"🏢 {row['name']} ({row['category']})"):
                    st.write(f"**📍 العنوان:** {row['location']}")
                    st.write(f"**📝 التفاصيل:** {row['details']}")
                    st.write(f"**📞 الاتصال:** {row['contact']}")
                found = True
        if not found:
            st.warning("للأسف، لسه مفيش موردين بالاسم ده في الداتابيز بتاعتنا.")

# =========================================================
# التبويب الثاني: محرك التسويق
# =========================================================
with tab2:
    st.header("مولد خطة التسويق الذكي")
    with st.form("marketing_form"):
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("اسم المشروع", placeholder="مثلاً: قهوة المزاج")
            industry = st.selectbox("مجال المشروع", ["مطاعم وكافيهات", "ملابس وأزياء", "عقارات", "خدمات طبية", "أخرى"])
        with col2:
            target_audience = st.text_input("الجمهور المستهدف", placeholder="مثلاً: طلبة الجامعات")
            goal = st.selectbox("هدف الخطة", ["زيادة مبيعات", "انتشار (Awareness)", "تفاعل (Engagement)"])
        
        submit_btn = st.form_submit_button("✨ توليد الخطة التسويقية")
    
    if submit_btn:
        if not project_name:
            st.warning("⚠️ من فضلك اكتب اسم المشروع الأول عشان أقدر أساعدك.")
        else:
            with st.spinner('جاري تحضير الخطة...'):
                try:
                    marketing_prompt = f"""
                    أنت مدير تسويق محترف.
                    المشروع: {project_name} ({industry})
                    الجمهور: {target_audience}
                    الهدف: {goal}
                    
                    المطلوب: جدول خطة محتوى لأول أسبوع (يوم، نوع المحتوى، السكريبت، وصف الصورة).
                    اكتب باللهجة المصرية.
                    """
                    response = model.generate_content(marketing_prompt)
                    st.success(f"خطة {project_name} جاهزة! 🎯")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"حصل خطأ في الاتصال: {e}")