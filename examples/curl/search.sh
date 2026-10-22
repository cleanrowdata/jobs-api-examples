#!/usr/bin/env bash
# Search ~17,500 company career sites in one call and save a CSV.
# Usage: APIFY_TOKEN=... ./search.sh "data engineer" "United States"
set -euo pipefail
: "${APIFY_TOKEN:?Set APIFY_TOKEN (Apify Console > Settings > API & Integrations)}"
TITLE="${1:-data engineer}"
LOCATION="${2:-United States}"
curl -s -X POST \
  "https://api.apify.com/v2/acts/cleanrowdata~fresh-jobs-index/run-sync-get-dataset-items?format=csv" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" -H "Content-Type: application/json" \
  -d "{\"timeRange\":\"24h\",\"titleSearch\":[\"${TITLE}\"],\"locationSearch\":[\"${LOCATION}\",\"Remote\"],\"limit\":50}" \
  -o jobs.csv
echo "Saved $(($(wc -l < jobs.csv) - 1)) rows to jobs.csv"
