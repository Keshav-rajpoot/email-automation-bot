import os, pandas as pd
from datetime import datetime

LOG_PATH = "logs/classified_emails.csv"
os.makedirs("logs", exist_ok=True)

COLUMNS = [
    "ts", "id", "threadId", "from", "subject", "date",
    "category", "replied", "reply_to"
]

def log_batch(results):
    rows = []
    now = datetime.utcnow().isoformat()
    for r in results:
        rows.append({
            "ts": now,
            "id": r["id"],
            "threadId": r["threadId"],
            "from": r["from"],
            "subject": r["subject"],
            "date": r["date"],
            "category": r.get("category",""),
            "replied": r.get("replied", False),
            "reply_to": r.get("reply_to",""),
        })
    df = pd.DataFrame(rows, columns=COLUMNS)
    header = not os.path.exists(LOG_PATH)
    df.to_csv(LOG_PATH, mode="a", index=False, header=header)

def summary_report():
    if not os.path.exists(LOG_PATH):
        print("No logs yet.")
        return
    df = pd.read_csv(LOG_PATH)
    by_cat = df.groupby("category")["id"].count().sort_values(ascending=False)
    by_day = df.assign(day=df["ts"].str[:10]).groupby("day")["id"].count()
    print("\n=== Volume by Category ===")
    print(by_cat.to_string())
    print("\n=== Volume by Day ===")
    print(by_day.to_string())
