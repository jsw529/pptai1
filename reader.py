import streamlit as st
import requests

st.title("📖 대본 읽어주는 AI 웹사이트")

SERVER_URL = "https://your-server-url.onrender.com"  # 여기에 본인 FastAPI 서버 주소 입력하세요!

uploaded_script = st.file_uploader("대본 (.txt) 파일 업로드", type=["txt"])

script_text = ""
if uploaded_script:
    script_text = uploaded_script.read().decode("utf-8")
    st.text_area("대본 미리보기", script_text, height=200)

st.subheader("목소리 선택")
voices = []
selected_voice = ""
try:
    res = requests.get(f"{SERVER_URL}/voices")
    if res.status_code == 200:
        voices = res.json()
        korean_voices = [v for v in voices if "ko-KR" in v["language_codes"]]
        if korean_voices:
            selected_voice = st.selectbox(
                "원하는 목소리를 선택하세요",
                options=[v["name"] for v in korean_voices]
            )
except:
    st.error("목소리 리스트를 불러올 수 없습니다. 서버 확인하세요!")

if st.button("🗣️ 읽기 시작"):
    if not script_text:
        st.warning("대본을 업로드하거나 작성해 주세요.")
    else:
        with st.spinner("AI가 읽는 중입니다..."):
            res = requests.post(
                f"{SERVER_URL}/synthesize",
                data={"text": script_text, "voice_name": selected_voice}
            )
            if res.status_code == 200:
                audio_bytes = res.content
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("음성 생성 실패!")
