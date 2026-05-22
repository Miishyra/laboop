import json
import os

FILE = "data.json"

def save(servers):
    data = []
    for s in servers:
        data.append({
            "name": s.name,
            "ip": s.ip,
            "cpu": s._cpu,
            "ram": s._ram,
            "status": s.status,
            "priority": s.priority,
            "connections": s.connections
        })
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)