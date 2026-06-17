from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

default_args = {
    'owner': 'dias',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD")
}

API_TOKEN = os.getenv("API_TOKEN")

def fetch_and_save():
    # получаем данные
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Ошибка API: {response.status_code}")

    matches = response.json()["matches"]

    # сохраняем в БД
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    inserted = 0
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
        inserted += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Обработано матчей: {inserted}")

# создаём DAG
with DAG(
    dag_id='football_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule='@daily',  # каждый день
    catchup=False
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_and_save_matches',
        python_callable=fetch_and_save
    )