# Job postings API examples: Greenhouse, Lever, Ashby and Workday jobs in one call

Copy-paste examples for pulling **fresh job postings straight from company career sites** (Greenhouse, Lever, Ashby, Workday, Workable, SmartRecruiters and more) with the CleanRow Data Actors on Apify. Python, JavaScript, curl and n8n.

> Maintained by **CleanRow Data** (Apify account [`cleanrowdata`](https://apify.com/cleanrowdata)). This repo holds examples only; the Actors run on Apify. Nothing in this repo needs a secret except your own `APIFY_TOKEN`, which you set as an environment variable.

## Why career sites instead of job boards?

Most jobs on LinkedIn and Indeed start in an applicant tracking system (ATS). The ATS feed is the source: it has the job first, it says when the job closed, and it has no reposts or staffing-agency copies. These Actors keep an hourly index of about 17,500 company boards (Workday daily), so you search all of them in one call instead of crawling 17,500 URLs yourself.

## Which Actor do I need?

| You want | Actor | Example input |
|---|---|---|
| Search all jobs across 17,500+ companies (title, location, salary, seniority, visa) | [Job Postings API](https://apify.com/cleanrowdata/fresh-jobs-index) | `{"timeRange":"24h","titleSearch":["data engineer"],"locationSearch":["United States","Remote"],"limit":100}` |
| Remote jobs filtered by where you can work from | [Remote Jobs API](https://apify.com/cleanrowdata/remote-jobs-api) | `{"timeRange":"7d","eligibleFrom":["europe"],"limit":100}` |
| Companies hiring right now (one row per company, for sales/recruiting leads) | [Hiring Signals API](https://apify.com/cleanrowdata/hiring-signals-api) | `{"timeRange":"7d","jobFunctions":["security"],"minNewJobs":3,"limit":100}` |
| Every job from a list of careers pages, with new/closed tracking | [Careers Page Jobs Scraper](https://apify.com/cleanrowdata/careers-jobs-feed) | `{"companies":["https://boards.greenhouse.io/airbnb","https://jobs.lever.co/spotify"],"changesOnly":true}` |
| Workday only (myworkdayjobs.com, 2,100+ companies) | [Workday Jobs Scraper](https://apify.com/cleanrowdata/workday-jobs-scraper) | `{"timeRange":"24h","companies":["Bank of America","Salesforce"],"limit":500}` |
| Greenhouse only (5,600+ companies) | [Greenhouse Jobs Scraper](https://apify.com/cleanrowdata/greenhouse-jobs-scraper) | `{"timeRange":"7d","titleSearch":["software engineer"],"limit":200}` |
| Lever only (1,700+ companies) | [Lever Jobs Scraper](https://apify.com/cleanrowdata/lever-jobs-scraper) | `{"timeRange":"7d","locationSearch":["United States"],"limit":200}` |
| Ashby only (3,200+ startups) | [Ashby Jobs Scraper](https://apify.com/cleanrowdata/ashby-jobs-scraper) | `{"timeRange":"all","companies":["OpenAI","Snowflake"],"limit":500}` |

Coverage numbers are from the Store listings as of October 2026 and change daily.

## Quick start (60 seconds)

1. Create a free Apify account (it includes monthly free credit) and copy your API token from **Settings → API & Integrations**.
2. `export APIFY_TOKEN=...` (never commit it).
3. Run one of these:

```bash
# curl: CSV of data-engineer jobs posted in the last 24h, US or remote
curl -s -X POST \
  "https://api.apify.com/v2/acts/cleanrowdata~fresh-jobs-index/run-sync-get-dataset-items?format=csv" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"timeRange":"24h","titleSearch":["data engineer"],"locationSearch":["United States","Remote"],"limit":50}' \
  -o jobs.csv
```

```bash
pip install apify-client
python examples/python/search_jobs.py
```

```bash
npm install apify-client
node examples/javascript/search-jobs.mjs
```

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/curl/search.sh`](examples/curl/search.sh) | One-call search, CSV out |
| [`examples/python/search_jobs.py`](examples/python/search_jobs.py) | Search the index, print a table |
| [`examples/python/daily_new_jobs.py`](examples/python/daily_new_jobs.py) | Daily "only new since last run" feed, written to CSV (cron or GitHub Actions) |
| [`examples/python/hiring_signals.py`](examples/python/hiring_signals.py) | Companies opening 3+ new roles in a function this week |
| [`examples/python/careers_watchlist.py`](examples/python/careers_watchlist.py) | Watch a list of careers pages for new and closed jobs |
| [`examples/python/workday_company_jobs.py`](examples/python/workday_company_jobs.py) | All open Workday jobs for named companies |
| [`examples/javascript/search-jobs.mjs`](examples/javascript/search-jobs.mjs) | Same search from Node.js |
| [`n8n/daily-new-jobs-to-google-sheets.json`](n8n/daily-new-jobs-to-google-sheets.json) | Importable n8n workflow: daily new jobs → Google Sheets |
| [`n8n/weekly-hiring-signals-to-google-sheets.json`](n8n/weekly-hiring-signals-to-google-sheets.json) | Importable n8n workflow: companies hiring 3+ in a function → Google Sheets |

## What a row looks like

```json
{
  "title": "Principal Software Engineer, Full Stack — Codex",
  "company": "OpenAI",
  "ats": "ashby",
  "location": "San Francisco",
  "remote": false,
  "posted_at": "2026-10-21T17:32:33Z",
  "first_seen": "2026-10-21T17:37:01Z",
  "status": "active",
  "salary_text": "$441K - $515K",
  "description": "About the Role ... (plain text)",
  "job_url": "https://jobs.ashbyhq.com/...",
  "apply_url": "https://jobs.ashbyhq.com/.../application"
}
```

Other fields include `company_domain`, `department`, `workplace_type`, `locations`, `country`, `employment_type`, `salary_min`, `salary_max`, `salary_currency`, `salary_period`, `last_seen` and `closed_at`. Full schema: the **Output** tab of each Actor.

## Pricing

Pay per job returned, platform usage included. On the Job Postings API: $2.50 per 1,000 jobs on Apify's free plan, down to $1.00 per 1,000 on Business. The examples here use `limit` values of 50–500, so a test run costs cents. Check each Actor's **Pricing** tab for the current numbers.

## Doing it yourself (no Actor)

For a single company you don't need any of this. The public endpoints:

```
GET  https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true
GET  https://api.lever.co/v0/postings/{company}?mode=json
GET  https://api.ashbyhq.com/posting-api/job-board/{company}
POST https://{tenant}.wd5.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs
     {"appliedFacets":{},"limit":20,"offset":0,"searchText":""}
```

The Actors are for when you need *search across thousands of companies*, closed-job tracking, deduplication and salary parsing without running the crawler.

## Limits

- Only companies on a supported ATS are covered (17,500+, not every employer).
- Workday boards refresh daily; the others hourly.
- Some Workday, SmartRecruiters, Recruitee, Personio and Rippling rows can have an empty `description`.

## Feedback

Missing a company, field or filter? Open an issue on the Actor's **Issues** tab on Apify (answered within a day), or open an issue here.

## License

MIT for the example code in this repo. The Actors themselves are hosted services on Apify.
