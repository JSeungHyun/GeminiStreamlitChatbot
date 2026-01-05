# app/chains.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchainhub import Client
from app.utils import load_prompt

# LCEL 문법을 사용하여 체인을 생성하는 함수
def create_chain(prompt_type="기본모드"):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0
    )
    
    # 2. 프롬프트 설정
    # 기본 프롬프트
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 AI 멘토입니다. 질문에 대해 명확하고 구조적으로 답변해주세요."),
        ("user", "#Question:\n{question}")
    ])

    # 선택에 따른 프롬프트 교체 로직
    if prompt_type == "블로그 게시글":
        # 파일이 없을 경우를 대비한 예외처리
        try:
            prompt = load_prompt("prompts/blog.yaml", encoding="utf-8")
        except Exception as e:
            # 파일이 없으면 그냥 기본 프롬프트 사용 (에러 방지)
            print(f"blog.yaml load 중 오류 발생 ⚠️ : {e}")
            pass 
            
    elif prompt_type == "요약":
        try:
            prompt = load_prompt("prompts/summary.yaml", encoding="utf-8")
        except Exception:
            print(f"summary.yaml load 중 오류 발생 ⚠️ : {e}")
            pass

    # 3. 출력 파서
    output_parser = StrOutputParser()

    # 4. 체인 연결 (LCEL: Prompt | LLM | OutputParser)
    chain = prompt | llm | output_parser
    
    return chain