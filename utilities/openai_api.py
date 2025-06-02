import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def openai_api(prompt):
    prompt = prompt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=200,
    )

    return response.choices[0].message.content


def find_dish(flavors, mains, staples):
    prompt = f"""
    根據以下口味（{','.join(flavors)}）、主餐（{','.join(mains)}）、主食（{','.join(staples)}），
    列出10道在台灣真實存在的常見料理名稱，用逗號分隔，不要加空格。
    例如：牛丼,咖哩豬排飯,打拋豬,麻辣火鍋...
    """
    return prompt
