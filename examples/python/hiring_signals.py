"""Companies that opened 3+ new roles in a function this week (one row per company).

Useful as a sales trigger: a company hiring 5 security engineers is likely buying security tools.
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("cleanrowdata/hiring-signals-api").call(run_input={
    "timeRange": "7d",
    "jobFunctions": ["security"],
    "locationSearch": ["United States"],
    "minNewJobs": 3,
    "limit": 100,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(row["company"], row.get("company_domain"), "new jobs:", row["new_jobs"], row.get("new_jobs_by_function"))
