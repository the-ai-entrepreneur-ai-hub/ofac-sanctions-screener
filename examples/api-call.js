import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_API_TOKEN' });

const input = {
    queries: ['Bank Melli Iran', 'Huawei Technologies', 'Apple Inc'],
    matchThreshold: 70,
    entityType: 'all',
};

const run = await client.actor('george.the.developer/ofac-sanctions-screener').call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();

for (const item of items) {
    console.log(`${item.queryName}: ${item.riskLevel} (${item.matchConfidence}% confidence)`);
}
