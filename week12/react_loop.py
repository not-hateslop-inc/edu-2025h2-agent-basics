import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, FUNCS

load_dotenv()
client = OpenAI()

def run(question, max_steps=5):
    messages = [{"role": "system", "content": "헤이트슬롭 사내 업무 도우미다. 필요하면 도구를 쓴다."},
                {"role": "user", "content": question}]
    for step in range(max_steps):
        msg = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=TOOLS).choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments or "{}")
            result = FUNCS[tc.function.name](**args)
            print(f"[step {step}] {tc.function.name}({args}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})
    return "최대 단계에 도달했습니다"

if __name__ == "__main__":
    print(run("오늘 8명 회의할 방 찾아줘. 날짜도 같이 알려줘."))
