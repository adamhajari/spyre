Steps:
---

1. work through google's [hello world example](https://cloud.google.com/python/getting-started/hello-world#deploy_and_run_hello_world_on_app_engine)
2. clone this repo and cd to repo's directory
3. test app locally
4. push repo to the google cloud repo
5. create instance with startup-script


## content of repo
1. startup script
2. spyre app
3. requirements.txt


```
gcloud compute instances create spyre-on-gcloud \
    --image-family=ubuntu-1404 \
    --machine-type=f1-micro \
    --metadata-from-file startup-script=startup-script.sh \
    --zone us-east1-b \
    --tags http-server \
    --project=spyre-example
```

gcloud compute instances create spyre-on-gcloud2 \
    --image=ubuntu-1404-trusty-v20171101 \
    --machine-type=f1-micro \
    --metadata-from-file startup-script=startup-script.sh \
    --zone us-east1-b \
    --tags http-server \
    --project=spyre-example

ubuntu-1404-trusty-v20171101