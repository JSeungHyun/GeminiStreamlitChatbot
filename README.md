# 🤖 Gemini Streamlit Chatbot (LangChain Practice)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green.svg)
![Gemini](https://img.shields.io/badge/Model-Gemini%201.5%20Flash-orange.svg)

LangChain과 Google Gemini Pro 모델을 활용하여 구축한 **대화형 챗봇 애플리케이션**입니다.  
사용자의 질문에 답변하는 기본 기능 외에 **블로그 포스팅 작성**, **텍스트 요약** 등 특화된 기능을 제공합니다.

> 💡 **Credit & Inspiration** > 이 프로젝트는 **['테디노트(TeddyNote)'의 LangChain 강의]**를 수강하며 학습한 내용을 바탕으로 제작되었습니다.  

---

## 📌 주요 기능 (Features)

1.  **기본 대화 모드 (Chat):** Google Gemini 2.5 Flash 모델 기반의 빠르고 자연스러운 대화
2.  **블로그 포스팅 생성 (Blog Generator):** 주제만 입력하면 SEO에 최적화된 블로그 글 구조(제목, 본문, 태그 등) 자동 생성
3.  **핵심 요약 (Summary Expert):** 긴 텍스트나 복잡한 내용을 입력받아 핵심 내용만 간결하게 요약
4.  **창의성 조절 (Parameter Tuning):** 사이드바의 Temperature 슬라이더를 통해 AI 답변의 창의성 수준(0.0 ~ 1.0)을 실시간으로 제어 ✅

---

## 📂 프로젝트 구조 (Directory Structure)

```bash
📦 my-gemini-project
 ┣ 📂 app
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 chains.py       # LangChain 체인 정의 및 Gemini 모델 설정
 ┃ ┗ 📜 utils.py        # YAML 프롬프트 로드 및 유틸리티 함수
 ┣ 📂 prompts
 ┃ ┣ 📜 blog.yaml       # 블로그 작성 페르소나 및 프롬프트 템플릿
 ┃ ┗ 📜 summary.yaml    # 요약 전문가 페르소나 및 프롬프트 템플릿
 ┣ 📜 .env              # API Key 환경변수 설정 (Git 제외)
 ┣ 📜 .gitignore        # 보안 및 불필요 파일 제외 설정
 ┣ 📜 main.py           # Streamlit UI 진입점
 ┗ 📜 requirements.txt  # 의존성 패키지 목록