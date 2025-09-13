from datetime import date

# Mock driver data (replace later with SQLite/Postgres ORM models)
driver_earnings = [
    {"date": date(2025, 9, 10), "earnings": 1500, "expenses": 300, "penalties": 0},
    {"date": date(2025, 9, 11), "earnings": 1800, "expenses": 400, "penalties": 100},
]

def get_today_net_income():
    today = driver_earnings[-1]
    return today["earnings"] - today["expenses"] - today["penalties"]

def get_last_week_growth():
    if len(driver_earnings) < 2:
        return 0
    return (driver_earnings[-1]["earnings"] - driver_earnings[-2]["earnings"]) / driver_earnings[-2]["earnings"] * 100
