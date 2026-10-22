"""Watch a list of careers pages and get only what changed (new + closed jobs) since the last run.

Paste careers URLs or company names; the Actor detects the ATS (Greenhouse, Lever, Ashby,
Workday, SmartRecruiters, Workable). Schedule it daily.
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("cleanrowdata/careers-jobs-feed").call(run_input={
    "companies": [
        "https://boards.greenhouse.io/airbnb",
        "https://jobs.lever.co/spotify",
        "https://jobs.ashbyhq.com/openai",
    ],
    "changesOnly": True,          # first run returns everything, later runs only new/closed
    "feedKey": "my-watchlist",    # keep stable between runs
    "includeDescriptionHtml": False,
})
for job in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(job["status"], job["company"], "|", job["title"])  # status: new / active / closed
