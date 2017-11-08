Steps:
---

1. work through google's [hello world example](https://cloud.google.com/python/getting-started/hello-world#deploy_and_run_hello_world_on_app_engine)
2. fork and clone the [spyre repo](https://github.com/adamhajari/spyre)
3. cd to spyre/tutorial/google_cloud
4. create instance with startup-script

gcloud compute instances create [INSTANCE-NAME] \
    --image=debian-8 \
    --machine-type=f1-micro \
    --metadata-from-file startup-script=startup-script.sh \
    --zone us-east1-b \
    --tags http-server \
    --project=[PROJECT_ID]

5. open up port 8080
gcloud compute firewall-rules create default-allow-http-8080 \
    --allow tcp:8080 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server \
    --description "Allow port 8080 access to http-server" \
    --project=[PROJECT_ID]


gcloud compute instances create sinewaveapp \
    --image=debian-8 \
    --machine-type=f1-micro \
    --metadata-from-file startup-script=startup-script.sh \
    --zone us-east1-b \
    --tags http-server \
    --project=spyre-example