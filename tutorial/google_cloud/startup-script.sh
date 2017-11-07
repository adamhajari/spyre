# [START startup]
set -v

# Talk to the metadata server to get the project id
PROJECTID=$(curl -s "http://metadata.google.internal/computeMetadata/v1/project/project-id" -H "Metadata-Flavor: Google")

# Install logging monitor. The monitor will automatically pickup logs sent to
# syslog.
# [START logging]
curl -s "https://storage.googleapis.com/signals-agents/logging/google-fluentd-install.sh" | bash
service google-fluentd restart &
# [END logging]

# # Install dependencies from apt
# apt-get update
# apt-get install -yq \
#     git build-essential supervisor libffi-dev libssl-dev

# Create a pythonapp user. The application will run as this user.
useradd -m -d /home/pythonapp pythonapp

# Get the source code from the Google Cloud Repository
# git requires $HOME and it's not set during the startup script.
export HOME=/root
git clone https://github.com/adamhajari/spyre.git /opt/app

#Download and install the miniconda distribution of python
wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh;
bash miniconda.sh -b -p /home/pythonapp/miniconda
chown -R pythonapp:pythonapp /home/pythonapp/miniconda/
export PATH="/home/pythonapp/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a
conda create -q -n app-env python=2.7 numpy matplotlib pandas

# Install app dependencies
/home/pythonapp/miniconda/envs/app-env/bin/pip install -r /opt/app/tutorial/google_cloud/requirements.txt

# Make sure the pythonapp user owns the application code
chown -R pythonapp:pythonapp /opt/app

# Configure supervisor to start gunicorn inside of our virtualenv and run the
# application.
cat >/etc/supervisor/conf.d/python-app.conf << EOF
[program:spyreexample]
directory=/opt/app/tutorial/google_cloud
command=/home/pythonapp/miniconda/envs/app-env/bin/python2.7 /opt/app/tutorial/google_cloud/app.py 0.0.0.0
autostart=true
autorestart=true
user=pythonapp
# Environment variables ensure that the application runs inside of the
# configured virtualenv.
environment=VIRTUAL_ENV="/home/pythonapp/miniconda/envs/app-env/",PATH="/opt/app/tutorial/google_cloud/env/bin",\
    HOME="/home/pythonapp",USER="pythonapp"
stdout_logfile=syslog
stderr_logfile=syslog
EOF

supervisorctl reread
supervisorctl update

# Application should now be running under supervisor
# [END startup]




#/home/pythonapp/miniconda/envs/app-env/bin/pip install -r /opt/app/tutorial/google_cloud/requirements.txt
