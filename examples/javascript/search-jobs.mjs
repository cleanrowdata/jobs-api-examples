// npm install apify-client
// APIFY_TOKEN=... node search-jobs.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('cleanrowdata/fresh-jobs-index').call({
  timeRange: '24h',
  titleSearch: ['frontend engineer', 'react'],
  locationSearch: ['Remote'],
  limit: 50,
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const job of items) {
  console.log(`${job.posted_at.slice(0, 16)}  ${job.company}  |  ${job.title}  |  ${job.location ?? ''}`);
}
