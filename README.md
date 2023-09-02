# Fetch_Rewards_DataEngineer
## Summary of the Code
The Python program periodically polls the SQS queue, fetches the JSON data from it in small batches, performs data cleaning to get the data into the required format and then finally places puts the data into the Postgres table

## Running the code
```
  git clone https://github.com/Kshitij6798/Fetch_Rewards_DataEngineer.git

  cd docker
```
  After navigating to the docker folder, compose the docker.yaml file using the command below
  
```
  docker-compose up -d
```

The two docker files should then be up and running. You can verify that by running the following command
```
docker ps
```



