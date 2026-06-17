import requests
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_matches():
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": os.getenv("API_TOKEN")}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Ошибка API: {response.status_code}")
        return []
    
    data = response.json()
    return data["matches"]

def save_matches(matches):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()
    
    inserted = 0
    skipped = 0

    for match in matches:
        cursor.execute("""
            INSERT INTO matches (external_id, match_date, home_team, away_team, score_home, score_away, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (external_id) DO UPDATE SET
                score_home = EXCLUDED.score_home,
                score_away = EXCLUDED.score_away,
                status = EXCLUDED.status
        """, (
            match["id"],
            match["utcDate"][:10],
            match["homeTeam"]["name"],
            match["awayTeam"]["name"],
            match["score"]["fullTime"]["home"],
            match["score"]["fullTime"]["away"],
            match["status"]
        ))

        if cursor.rowcount == 1:
            inserted += 1
        else:
            skipped += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Добавлено: {inserted} | Обновлено: {skipped}")

def run():
    matches = get_matches()
    if matches:
        save_matches(matches)

run()