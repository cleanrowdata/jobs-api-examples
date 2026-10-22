"""All open Workday jobs for named companies, matched by real company name (no tenant codes)."""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("cleanrowdata/workday-jobs-scraper").call(run_input={
    "timeRange": "all",
    "companies": [
        "Bank of America",
        "Salesforce",
        "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite",
    ],
    "limit": 1000,
})
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"{len(items)} jobs")
for job in items[:20]:
    print(job["company"], "|", job["title"], "|", job.get("location"))
