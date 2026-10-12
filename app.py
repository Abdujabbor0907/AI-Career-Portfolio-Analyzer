import os
import streamlit as st
import openai

st.set_page_config(page_title="AI Career & Portfolio Analyzer", page_icon="💼", layout="wide")

st.title("💼 AI Career & Portfolio Reviewer")
st.write("Rezyume va portfoliongizni AI orqali professional tahlil qiling hamda shaxsiy maslahatlar oling!")

# OpenAI API kalitini kiritish
api_key = st.sidebar.text_input("OpenAI API kalitingizni kiriting:", type="password")

if not api_key:
    st.info("💡 Ishni boshlash uchun chap paneldagi maydonga OpenAI API kalitingizni kiriting.")
    st.stop()

openai.api_key = api_key

# Ma'lumotlarni kiritish maydoni
col1, col2 = st.columns(2)

with col1:
    resume_text = st.text_area("Rezyume yoki tajribangiz matnini bu yerga joylang:", height=250, 
                               placeholder="Masalan: IT sohasida 3 yillik tajriba, Python, SQL bilaman, loyihalarda qatnashganman...")

with col2:
    target_job = st.text_input("Maqsad qilgan vakansiya/lavozimingiz:", placeholder="Masalan: Senior Python Developer yoki Project Manager")
    mode = st.selectbox("Nima qilish kerak?", [
        "Rezyumeni to'liq tahlil qilish (SWOT-analiz)",
        "Tavsiyanoma xati (Cover Letter) yaratish",
        "LinkedIn profilini yaxshilash bo'yicha maslahatlar"
    ])

if st.button("🚀 AI orqali tahlil qilish"):
    if not resume_text:
        st.warning("Iltimos, rezyume matnini kiriting!")
    else:
        with st.spinner("AI profilingizni tahlil qilmoqda..."):
            try:
                prompt = f"""
                Siz professional HR-ekspert va karera maslahatchisiz.
                Foydalanuvchi rezyumesi: {resume_text}
                Maqsad qilgan lavozimi: {target_job if target_job else 'Ko'rsatilmadi'}
                Vazifa: {mode}

                Aniq, tushunarli va foydali javob qaytaring. Asosiy punktlarni ajratib ko'rsating.
                """
                
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                result = response.choices[0].message.content
                st.success("Tahlil yakunlandi!")
                st.markdown("---")
                st.markdown("### 📊 Tahlil natijasi:")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {e}")