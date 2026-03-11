/**
 * OFAC Sanctions Screener — Node.js API Example
 *
 * Screen entities against the US Treasury OFAC SDN sanctions list
 * using the Apify API client.
 *
 * Install: npm install apify-client
 * Run:     node nodejs-api.js
 *
 * Get your API token at: https://console.apify.com/account/integrations
 * Actor:   https://apify.com/george.the.developer/ofac-sanctions-screener
 */

import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });

// Entities to screen against the OFAC SDN sanctions list
const input = {
    queries: [
        'Bank Melli Iran',       // Known sanctioned entity
        'Gazprombank',           // Known sanctioned entity
        'Rosneft Oil Company',   // Known sanctioned entity
        'Apple Inc',             // Should return CLEAR
        'Microsoft Corporation', // Should return CLEAR
    ],
    matchThreshold: 70,      // Minimum confidence score (70+ recommended)
    includeAliases: true,    // Also match against known aliases (AKAs)
    entityType: 'all',       // Filter: all, individual, entity, vessel, aircraft
    maxMatchesPerQuery: 5,   // Max matches per entity
};

console.log(`Screening ${input.queries.length} entities against OFAC SDN list...\n`);

const run = await client.actor('george.the.developer/ofac-sanctions-screener').call(input);

console.log(`Run finished. Status: ${run.status}`);
console.log(`Dataset ID: ${run.defaultDatasetId}\n`);

// Fetch results
const { items } = await client.dataset(run.defaultDatasetId).listItems();

// Display results
for (const item of items) {
    const status = item.riskLevel === 'CLEAR' ? 'CLEAR' : `MATCH (${item.riskLevel})`;
    const confidence = item.matchConfidence ?? 0;

    console.log(`${item.queryName}: ${status} — ${confidence}% confidence`);

    if (item.matchedName) {
        console.log(`  Matched: ${item.matchedName}`);
        console.log(`  Programs: ${item.programs?.join(', ') || 'N/A'}`);
        console.log(`  Aliases: ${item.aliases?.slice(0, 3).join(', ') || 'N/A'}`);
    }
    console.log('');
}

// Export full results as JSON
console.log('--- Full JSON Output ---');
console.log(JSON.stringify(items, null, 2));
