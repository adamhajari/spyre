google-api-python-client
google-cloud-bigquery
pandas-gbq

gcloud compute instances create weatherhistory \
     --image-family=debian-8 \
     --image-project=debian-cloud \
     --machine-type=f1-micro \
     --metadata-from-file startup-script=startup-script.sh \
     --zone us-east1-b \
     --tags http-server \
     --scopes=[bigquery] \
     --project=spyre-example

