import requests
from bs4 import BeautifulSoup

URL = "https://e2finc.hrmdirect.com/employment/job-openings.php?search=true&&cust_sort1=247739"
BASE_URL = "https://e2finc.hrmdirect.com"


def fetch_jobs():
    print("Fetching jobs...")
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    rows = soup.find_all("tr", class_=lambda c: c and "reqitem" in c)

    for row in rows:
        job_type_cell = row.find("td", class_="custSort1")
        title_cell = row.find("td", class_="posTitle")
        country_cell = row.find("td", class_="countries")

        if not title_cell:
            continue

        link = title_cell.find("a", href=True)
        if not link:
            continue

        job_type = job_type_cell.get_text(strip=True) if job_type_cell else ""
        title = link.get_text(strip=True)
        country = country_cell.get_text(strip=True) if country_cell else ""

        href = link["href"]
        full_url = BASE_URL + href if href.startswith("/") else href

        jobs.append({
            "title": title,
            "url": full_url,
            "job_type": job_type,
            "country": country
        })

    print(f"Found {len(jobs)} job(s) on the page.")

    if not jobs:
        raise RuntimeError(
            "Scraper found 0 jobs on the page. This likely means the site's "
            "HTML structure changed and the scraper needs updating."
        )

    return jobs
