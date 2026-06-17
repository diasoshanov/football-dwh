import requests
import json

API_TOKEN = "8f7986d911394754b7469079eb9fbadd"

def get_matches():
    url = "https://api.football-data.org/v4/competitions/WC/matches"  # АПЛ
    headers = {"X-Auth-Token": API_TOKEN}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        matches = data["matches"]
        
        for match in matches[:5]:  # первые 5 матчей
            home = match["homeTeam"]["name"]
            away = match["awayTeam"]["name"]
            date = match["utcDate"][:10]
            status = match["status"]
            score_hometeam = match["score"]["fullTime"]["home"]
            score_awayteam = match["score"]["fullTime"]["away"]
            print(f"{date} | {home} vs {away} | {score_hometeam}:{score_awayteam} | {status}")
    else:
        print(f"Ошибка: {response.status_code}")

get_matches()