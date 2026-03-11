from apify_client import ApifyClient

client = ApifyClient('YOUR_API_TOKEN')

run = client.actor('george.the.developer/ofac-sanctions-screener').call(run_input={
    'queries': ['Bank Melli Iran', 'Huawei Technologies', 'Apple Inc'],
    'matchThreshold': 70,
    'entityType': 'all',
})

for item in client.dataset(run['defaultDatasetId']).iterate_items():
    print(f"{item['queryName']}: {item['riskLevel']} ({item['matchConfidence']}% confidence)")
