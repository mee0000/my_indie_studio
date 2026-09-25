import os
import requests
from pathlib import Path
from dotenv import load_dotenv
# .env 파일에서 API Key 읽어오기 (python-dotenv 패키지 미설치 시 환경변수 직접 참조)

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def generate_code_with_deepseek(prompt_text: str):
    if not DEEPSEEK_API_KEY:
        print("❌ Error: DEEPSEEK_API_KEY가 .env 또는 환경변수에 설정되지 않았습니다.")
        return

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    payload = {
        "model": "deepseek-coder",
        "messages": [
            {"role": "system", "content": "You are an expert full-stack developer specializing in FastAPI and Vue 3."},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.2
    }

    print("🤖 Agent가 코드를 생성하고 있습니다...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        generated_code = result['choices'][0]['message']['content']
        print("\n=== 生成된 코드 ===\n")
        print(generated_code)
        return generated_code
    except Exception as e:
        print(f"❌ API 호출 중 오류 발생: {e}")

if __name__ == "__main__":
    test_prompt = "Create a simple FastAPI health check endpoint."
    generate_code_with_deepseek(test_prompt)