curl "https://api.apify.com/v2/acts/george.the.developer~ofac-sanctions-screener/run-sync-get-dataset-items?token=YOUR_API_TOKEN" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["Bank Melli Iran", "Huawei Technologies"],
    "matchThreshold": 70
  }'
