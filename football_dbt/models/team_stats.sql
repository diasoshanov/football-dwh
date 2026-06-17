WITH home_goals AS (
    SELECT 
        home_team as team,
        COUNT(*) as matches_played,
        SUM(score_home) as goals_scored,
        SUM(CASE WHEN score_home > score_away THEN 1 ELSE 0 END) as wins,
        SUM(CASE WHEN score_home = score_away THEN 1 ELSE 0 END) as draws,
        SUM(CASE WHEN score_home < score_away THEN 1 ELSE 0 END) as losses
    FROM {{ source('public', 'matches') }}
    WHERE status = 'FINISHED'
    GROUP BY home_team
),

away_goals AS (
    SELECT 
        away_team as team,
        COUNT(*) as matches_played,
        SUM(score_away) as goals_scored,
        SUM(CASE WHEN score_away > score_home THEN 1 ELSE 0 END) as wins,
        SUM(CASE WHEN score_away = score_home THEN 1 ELSE 0 END) as draws,
        SUM(CASE WHEN score_away < score_home THEN 1 ELSE 0 END) as losses
    FROM {{ source('public', 'matches') }}
    WHERE status = 'FINISHED'
    GROUP BY away_team
)

SELECT
    team,
    SUM(matches_played) as matches_played,
    SUM(goals_scored) as goals_scored,
    SUM(wins) as wins,
    SUM(draws) as draws,
    SUM(losses) as losses
FROM (
    SELECT * FROM home_goals
    UNION ALL
    SELECT * FROM away_goals
) combined
GROUP BY team
ORDER BY goals_scored DESC