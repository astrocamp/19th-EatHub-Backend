from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def openai_api(prompt):
    prompt = prompt
    response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': prompt}],
    temperature=0.8,
    max_tokens=200,
    )
    return response.choices[0].message.content

def find_dish(flavors, mains, staples):
    prompt = f"""
你是一位熟悉台灣日常餐廳菜單的美食推薦助手。

請**從真實存在的台灣常見料理中**，挑選出 10 道菜，這些菜需**各自符合下列三類條件中的任意兩項以上**（非三項全中也可）。

條件：
1. 調味風格：{', '.join(flavors)}
2. 主食材：{', '.join(mains)}
3. 主食類型：{', '.join(staples)}

⚠️ 請遵守以下規則：
- **只能挑選現實中台灣常見的料理名稱**，不要創造新菜名
- 名稱應為台灣菜單常見形式，例如：咖哩雞排飯、壽喜燒牛丼、酸菜白肉鍋、韓式炸雞便當、蔥爆羊肉
- 僅輸出料理名稱，以半形逗號 `,` 分隔，不要有換行或其他說明
- 嚴格避免虛構名稱（如「麻辣水餃」、「香煎牛肉比薩」、「日式羊肉煲」等）

先從你知道的常見台灣餐廳料理中挑選，再篩選是否符合條件。
    """
    return prompt
