# app/chains.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchainhub import Client
from app.utils import load_prompt

# LCEL 문법을 사용하여 체인을 생성하는 함수
def create_chain(prompt_type="기본모드", temperature=0):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=temperature
    )
    
    # 2. 프롬프트 텍스트 설정
    template_text = ""
    if prompt_type == "블로그 게시글":
        try:
            prompt_obj = load_prompt("prompts/blog.yaml", encoding="utf-8")
            template_text = prompt_obj.template
        except Exception as e:
            print(f"blog.yaml load 중 오류 발생 ⚠️ : {e}")
            template_text = "당신은 친절한 AI 멘토입니다.\n#Question:\n{question}"
            
    elif prompt_type == "요약":
        try:
            prompt_obj = load_prompt("prompts/summary.yaml", encoding="utf-8")
            template_text = prompt_obj.template
        except Exception as e:
            print(f"summary.yaml load 중 오류 발생 ⚠️ : {e}")
            template_text = "당신은 요약 전문가입니다.\n#Question:\n{question}"
            
    else:
        # 기본 프롬프트
        template_text = (
            "당신은 친절한 AI 멘토입니다. 질문에 대해 명확하고 구조적으로 답변해주세요.\n"
            "#Question:\n{question}"
        )

    # 3. 메시지 생성 함수 (멀티모달 처리)
    def prepare_messages(input_dict):
        question = input_dict.get("question", "")
        image_file = input_dict.get("image_data")
        
        # 텍스트 포맷팅
        try:
            formatted_text = template_text.format(question=question)
        except KeyError:
            formatted_text = template_text + f"\n\nQuestion: {question}"
            
        content = [{"type": "text", "text": formatted_text}]
        
        # 이미지 처리
        if image_file:
            import base64
            # Streamlit UploadedFile -> bytes -> base64
            image_bytes = image_file.getvalue()
            b64_string = base64.b64encode(image_bytes).decode("utf-8")
            mime_type = image_file.type
            
            content.append({
                "type": "image_url",
                "image_url": f"data:{mime_type};base64,{b64_string}"
            })
            
        return [HumanMessage(content=content)]

    # 4. 출력 파서
    output_parser = StrOutputParser()

    # 5. 체인 연결 (RunnableLambda | LLM | OutputParser)
    from langchain_core.runnables import RunnableLambda
    from langchain_core.messages import HumanMessage
    
    chain = RunnableLambda(prepare_messages) | llm | output_parser
    
    return chain