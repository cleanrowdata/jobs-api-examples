"""Search ~17,500 company career sites (Greenhouse, Lever, Ashby, Workday, ...) in one call.

pip install apify-client
export APIFY_TOKEN=...   # Apify Console > Settings > API & Integrations
python search_jobs.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run_input = {
    "timeRange": "24h",                      # 1h, 24h, 7d, 30d or all
    "titleSearch": ["data engineer", "analytics engineer"],
    "locationSearch": ["United States", "Remote"],
    "excludeReposts": True,
    "includeDescription": False,             # True adds the full plain-text description
    "limit": 50,                             # you pay per job returned; keep it small while testing
}

run = client.actor("cleanrowdata/fresh-jobs-index").call(run_input=run_input)
for job in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f'{job["posted_at"][:16]}  {job["company"][:24]:24}  {job["title"][:60]:60}  {job.get("location") or ""}')
