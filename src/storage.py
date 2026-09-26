import json
import os

SEEN_JOBS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "seen_jobs.json")


def load_seen_jobs():
    if not os.path.exists(SEEN_JOBS_PATH):
        return set()
    with open(SEEN_JOBS_PATH, "r", encoding="utf-8") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()


def save_seen_jobs(seen_jobs):
    with open(SEEN_JOBS_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(seen_jobs), f, indent=2)
