# Fetch_Rewards_DataEngineer
## Summary of the Code
The Python program periodically polls the SQS queue, fetches the JSON data from it in small batches, performs data cleaning to get the data into the required format and then finally places puts the data into the Postgres table
