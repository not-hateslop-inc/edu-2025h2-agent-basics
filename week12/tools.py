import datetime

ROOMS = {"A": "4층 대회의실 (12인)", "B": "4층 소회의실 (6인)", "C": "5층 세미나실 (30인)"}

def get_today() -> str:
    return datetime.date.today().isoformat()

def find_room(people: int) -> str:
    for k, v in ROOMS.items():
        cap = int(v.split("(")[1].rstrip("인)"))
        if cap >= people:
            return f"{k}: {v}"
    return "수용 가능한 회의실이 없습니다"

TOOLS = [
    {"type": "function", "function": {"name": "get_today", "description": "오늘 날짜를 YYYY-MM-DD로 돌려준다", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "find_room", "description": "인원 수에 맞는 사내 회의실을 찾는다",
        "parameters": {"type": "object", "properties": {"people": {"type": "integer"}}, "required": ["people"]}}},
]
FUNCS = {"get_today": get_today, "find_room": find_room}
