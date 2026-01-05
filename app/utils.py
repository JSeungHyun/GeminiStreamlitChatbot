# app/utils.py
import yaml
from langchain_core.prompts import PromptTemplate

def load_prompt(file_path, encoding="utf-8"):
    # 1. 파일 열기
    with open(file_path, "r", encoding=encoding) as f:
        config = yaml.safe_load(f)
        
    # 2. 프롬프트 객체 생성 (복잡한 로딩 함수 없이 직접 생성)
    return PromptTemplate(
        template=config["template"],
        input_variables=config["input_variables"]
    )