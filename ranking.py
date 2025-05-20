import json
import os

RANKING_FILE = "ranking.json"

def load_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    with open(RANKING_FILE, "r") as f:
        return json.load(f)

def save_score(initials, score):
    ranking = load_ranking()
    ranking.append({"initials": initials, "score": score})
    ranking.sort(key=lambda x: x["score"], reverse=True)
    ranking = ranking[:10]  # mantém top 10
    with open(RANKING_FILE, "w") as f:
        json.dump(ranking, f)

def get_formatted_ranking():
    ranking = load_ranking()
    return [f"{entry['initials']} - {entry['score']}" for entry in ranking]
