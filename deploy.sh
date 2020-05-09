echo -e "3\nEarlyBirdTest1\nY\n1\nN\nn\n" | eb init -i
eb create EarlyBirdTest1-App
eb create -t worker EarlyBirdTest1-Worker
aws codepipeline create-pipeline --cli-input-json file://pipeline.json
aws codepipeline create-pipeline --cli-input-json file://pipeline_worker.json
