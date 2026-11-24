import sys
import traceback

from scraper import fetch_jobs
from storage import load_seen_jobs, save_seen_jobs
from notifier import send_email, send_failure_alert


def run():
    print("Job Alert Bot Started")

    seen_jobs = load_seen_jobs()
    print(f"Loaded {len(seen_jobs)} previously seen job(s).")

    current_jobs = fetch_jobs()
    new_jobs = [job for job in current_jobs if job["url"] not in seen_jobs]

    if new_jobs:
        print(f"{len(new_jobs)} new job(s) found!")

        # Send first. Only mark jobs as seen after successful delivery,
        # so a temporary email failure does not permanently lose alerts.
        send_email(new_jobs)

        for job in new_jobs:
            seen_jobs.add(job["url"])
        save_seen_jobs(seen_jobs)
        print(f"Saved {len(new_jobs)} newly notified job(s).")
    else:
        print("No new jobs found.")

    print("Done!")


def main():
    try:
        run()
    except Exception:
        error_message = traceback.format_exc()
        print("FATAL ERROR:")
        print(error_message)
        send_failure_alert(error_message)
        sys.exit(1)


if __name__ == "__main__":
    main()
