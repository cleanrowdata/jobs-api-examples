"""Daily feed of jobs you haven't seen yet, appended to new_jobs.csv.

Run it once a day (cron, GitHub Actions, or an Apify schedule). `onlyNewSinceLastRun`
plus a fixed `stateKey` makes the Actor remember what it already returned, so each run
only bills for genuinely new jobs.
"""
import csv
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run_input = {
    "timeRange": "7d",
    "titleSearch": ["product manager"],
    "locationSearch": ["United States", "Remote"],
    "seniority": ["senior", "staff_principal"],
    "onlyNewSinceLastRun": True,
    "stateKey": "pm-us-senior",      # any name; keep it stable between runs
    "limit": 500,
}

run = client.actor("cleanrowdata/fresh-jobs-index").call(run_input=run_input)
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())

fields = ["posted_at", "company", "title", "location", "salary_text", "ats", "job_url"]
new_file = not os.path.exists("new_jobs.csv")
with open("new_jobs.csv", "a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    if new_file:
        w.writeheader()
    w.writerows(rows)
print(f"{len(rows)} new jobs appended to new_jobs.csv")
