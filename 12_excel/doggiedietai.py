import pandas as pd
from openai import OpenAI
import os

# こちらのpyファイルはサンプルです

# こちらはxlsxにする
profile = pd.DataFrame([{
    "이름": "베르", "품종": "골든리트리버", "몸무게": "25kg", "나이": "10m", "기저질환": "관절염"
}])

daily_logs = pd.DataFrame([
    {"음식": "royal canin maxi puppy", "칼로리": 400, "단백질": "30g", "양": "100g"},
    {"음식": "닭가슴살", "칼로리": 150, "단백질": "25g", "양": "80g"}
])

total_calories = daily_logs['칼로리'].sum()
dog_info = profile.iloc[0].to_dict()

prompt = f"""
당신은 베테랑 수의사이자 영양사입니다. 아래 반려견 정보를 바탕으로 오늘 식단을 평가하고 조언해주세요.

[반려견 프로필]
이름: {dog_info['이름']}, 품종: {dog_info['품종']}, 몸무게: {dog_info['몸무게']}, 기저질환: {dog_info['기저질환']}

[오늘 현재까지 섭취량]
총 칼로리: {total_calories}kcal
상세 내역:
{daily_logs.to_string()}

질문: 오늘 저녁에 무엇을 얼마나 더 먹여야 할까요? 특히 기저질환을 고려해 주의점도 알려주세요.
"""

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)