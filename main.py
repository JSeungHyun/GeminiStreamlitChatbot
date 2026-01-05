# main.py
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages.chat import ChatMessage

# [핵심] 우리가 분리한 파일에서 함수 가져오기
from app.chains import create_chain

# 1. 환경변수 로드
load_dotenv()

# 2. 화면 설정
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("Gemini 챗봇 🤖")

# 3. 세션 상태(대화 기록) 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 4. 사이드바 UI
with st.sidebar:
    clear_btn = st.button("대화 초기화")
    selected_prompt = st.selectbox(
        "모드 선택", 
        ("기본모드", "블로그 게시글", "요약"), 
        index=0
    )
    
    # Temperature 슬라이더 추가
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

# 대화 기록 초기화 동작
if clear_btn:
    st.session_state["messages"] = []

# 5. 함수 정의 (화면에 뿌려주는 역할만 수행)
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

def add_message(role, content):
    st.session_state["messages"].append(ChatMessage(role=role, content=content))

# 6. 메인 로직 실행
print_messages()

# 사용자 입력 처리
user_input = st.chat_input("궁금한 내용을 물어보세요!")

if user_input:
    # 사용자 메시지 화면 표시
    st.chat_message("user").write(user_input)
    
    # AI 응답 생성 (스트리밍)
    with st.chat_message("assistant"):
        container = st.empty()
        ai_answer = ""
        
        # 1. 로딩 인디케이터 표시
        with st.spinner("답변을 생성하는 중입니다..."):
            try:
                # [중요] app/chains.py에서 가져온 함수로 체인 생성
                chain = create_chain(selected_prompt, temperature)
                
                # 2. 스트리밍 출력 (빈 컨테이너 활용)
                for token in chain.stream({"question": user_input}):
                    ai_answer += token
                    container.markdown(ai_answer)
                
                # 3. 완료 알림 표시
                st.toast("답변 생성이 완료되었습니다!", icon="✅")
                
            except Exception as e:
                st.error(f"에러 발생: {e}")
                ai_answer = "죄송합니다. 처리 중 오류가 발생했습니다."

    # 대화 기록 저장
    add_message("user", user_input)
    add_message("assistant", ai_answer)