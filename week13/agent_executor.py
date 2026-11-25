import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent

load_dotenv()

@tool
def get_today() -> str:
    """오늘 날짜를 YYYY-MM-DD로 돌려준다."""
    return datetime.date.today().isoformat()

@tool
def find_room(people: int) -> str:
    """인원 수에 맞는 사내 회의실을 찾는다."""
    return "B: 4층 소회의실 (6인)" if people <= 6 else "A: 4층 대회의실 (12인)" if people <= 12 else "C: 5층 세미나실 (30인)"

prompt = ChatPromptTemplate.from_messages([
    ("system", "헤이트슬롭 사내 업무 도우미다."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = create_tool_calling_agent(llm, [get_today, find_room], prompt)
executor = AgentExecutor(agent=agent, tools=[get_today, find_room], verbose=True, max_iterations=5)

if __name__ == "__main__":
    print(executor.invoke({"input": "오늘 8명 회의할 방 찾아줘"})["output"])
