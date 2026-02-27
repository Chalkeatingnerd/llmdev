import requests
import os
from openai import OpenAI
from dotenv import load_dotenv

# API & Client settings
load_dotenv()
client = OpenAI(api_key=os.environ['API_KEY'])
MODEL_NAME = "gpt-4o-mini"
WIKI_API_URL = "https://ja.wikipedia.org/w/api.php" 

# utilize wikipedia API
def get_medical_info(disease_name):
    params = {
        "action": "query",
        "format": "json",
        "titles": disease_name,
        "prop": "extracts",
        "explaintext": True,
        "exintro": True # extract intro for data utilization efficiency
    }
    response = requests.get(WIKI_API_URL, params=params)
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})
    return page.get("extract", "관련 정보를 찾을 수 없습니다.")

# solution
def generate_solutions(dog_profile, medical_data):
    prompt = f"""
    당신은 전문 수의사입니다. 제공된 정보를 바탕으로 이 반려견을 위한 맞춤형 치료 및 관리 솔루션을 3~4가지 제시하세요.
    각 솔루션은 학술적 근거(제공된 데이터)에 기반해야 합니다.

    [반려견 프로필]
    {dog_profile}

    [학술 정보 요약]
    {medical_data}

    조건:
    - 수술적 방법, 비수술적 방법(재활/운동), 영양 요법 등을 골고루 포함할 것.
    - 반려견의 나이와 몸무게를 고려할 것.
    """
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3 # for data accuracy
    )
    return response.choices[0].message.content

def main():
    # input data
    dog_name = "베르"
    dog_profile = "견종: 골든리트리버, 나이:10개월, 몸무게: 25kg, 현재 증상: 고관절 이형성증(CHD)"
    disease_keyword = "股関節形成不全" 

    print(f"[{dog_name}]를 위한 최신 치료 정보를 수집 중입니다...")
    
    # 데이터 스크래핑
    scraped_info = get_medical_info(disease_keyword)
    
    # LLM 분석 및 결과 도출
    solutions = generate_solutions(dog_profile, scraped_info)
    
    print("\n=== 추천 치료 및 관리 솔루션 ===")
    print(solutions)

if __name__ == "__main__":
    main()