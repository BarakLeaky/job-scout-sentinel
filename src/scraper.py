import requests

# E2F has moved its careers listings from HRMDirect to ClearCompany.
API_URL = "https://app.clearcompany.com/api/v2/jobs/e2finc/json"


def fetch_jobs():
    print("Fetching jobs from ClearCompany...")

    response = requests.get(
        API_URL,
        headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "ClearCompany did not return valid JSON. The careers feed may have changed."
        ) from exc

    # The ClearCompany public feed currently returns a list of job records.
    if isinstance(data, dict):
        data = data.get("Jobs") or data.get("jobs") or data.get("data") or []

    if not isinstance(data, list):
        raise RuntimeError(
            f"Unexpected ClearCompany response format: {type(data).__name__}"
        )

    jobs = []
    for item in data:
        if not isinstance(item, dict):
            continue

        title = (item.get("PositionTitle") or item.get("positionTitle") or "").strip()
        url = (
            item.get("ApplyUrl")
            or item.get("LegacyCareersUrl")
            or item.get("applyUrl")
            or ""
        ).strip()

        if not title or not url:
            continue

        jobs.append({
            "title": title,
            "url": url,
            "job_type": (
                item.get("JobType")
                or item.get("EmploymentType")
                or item.get("DepartmentName")
                or ""
            ),
            "country": (
                item.get("OfficeName")
                or item.get("CountryCode")
                or ""
            ),
        })

    print(f"Found {len(jobs)} job(s) in the ClearCompany feed.")

    if not jobs:
        raise RuntimeError(
            "ClearCompany returned zero usable jobs. Check the feed URL and response format."
        )

    return jobs
