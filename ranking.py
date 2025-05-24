import json
import os

RANKING_FILE = "ranking.json"

# Abre o arquivo JSON
def load_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    with open(RANKING_FILE, "r") as f:
        return json.load(f)

# Carrega o JSON do ranking e adiciona um novo objeto com as inciais e a pontuação
def save_score(initials, score):
    ranking = load_ranking()
    ranking.append({"initials": initials, "score": score})
    ranking.sort(key=lambda x: x["score"], reverse=True)
    ranking = ranking[:5]
    with open(RANKING_FILE, "w") as f:
        json.dump(ranking, f)

# Pega o ranking formatado
def get_formatted_ranking():
    ranking = load_ranking()
    return [f"{entry['initials']} - {entry['score']}" for entry in ranking]
