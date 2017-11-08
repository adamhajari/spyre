Deploying a Spyre App to Google Cloud
===

Check out the blog post on this tutorial [here](http://adamhajari.github.io/2017/11/08/deploying-a-spyre-app-on-google-cloud.html).

Before getting started with this tutorial work through Google's [hello world example](https://cloud.google.com/python/getting-started/hello-world#deploy_and_run_hello_world_on_app_engine) to get familiar with creating a project and working with the Google Cloud SDK (if you can't get the SDK working, don't worry, there's a work around). 

## Creating an instance

You can create your instance from the command line using the Google Compute SDK by running the following command from the directory where `startup-script.sh` is located:

```bash
gcloud compute instances create [INSTANCE-NAME] \
    --image-family=debian-8 \
    --image-project=debian-cloud \
    --machine-type=f1-micro \
    --metadata-from-file startup-script=startup-script.sh \
    --zone us-east1-b \
    --tags http-server \
    --project=[PROJECT_ID]
```

replacing [INSTANCE-NAME] with a name for your instance (you can call it anything), and [PROJECT_ID] with the project id for an existing project (You can use the same one you used the hello world example or create a new one). The command should finish running in a few seconds and you'll get an output giving some details about your instance. Here's what my command and output looked like:

```bash
$ gcloud compute instances create sinewaveapp \
>     --image-family=debian-8 \
>     --image-project=debian-cloud \
>     --machine-type=f1-micro \
>     --metadata-from-file startup-script=startup-script.sh \
>     --zone us-east1-b \
>     --tags http-server \
>     --project=spyre-example
Created [https://www.googleapis.com/compute/v1/projects/spyre-example/zones/us-east1-b/instances/sinewaveapp].
NAME         ZONE        MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP    STATUS
sinewaveapp  us-east1-b  f1-micro                   10.142.0.4   35.190.191.17  RUNNING
```

If you are having trouble with the Google Compute SDK, you can also create an instance from the [Google Compute Engine web console](https://console.cloud.google.com/compute/instancesAdd). Just make sure the machine type and boot disk match what's above and copy and past the contents of `startup-script.sh` to the startup script text box.

## Making your instance available to external traffic
It will take several minutes for our app to install everything and start running. In the meantime we'll need to open up port 8080 to external traffic. Do so by running this command (replacing [PROJECT_ID] with your project id):

```bash
gcloud compute firewall-rules create default-allow-http-8080 \
    --allow tcp:8080 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server \
    --description "Allow port 8080 access to http-server" \
    --project=[PROJECT_ID]
```

If you choose to launch your app from the web console you don't need to do this extra step. Instead, make sure to check the "Allow HTTP traffic" box when creating your instance.


You should now see your instance in the Compute Engine web console. You can open a terminal window for your instance directly in the browser from the `SSH` drop down menu. View your instance's logs by clicking the three vertical dots to the left of the `SSH` drop down.

If all goes well you can access your app by browsing to [ExternalIP]:8080. For instance, my External IP was 35.190.191.17, so my app was available at http://35.190.191.17:8080.
