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

# Install dependencies from apt
apt-get update
apt-get install -yq \
    git build-essential supervisor python python-dev python-pip libffi-dev \
    libssl-dev python-pandas

# Create a pythonapp user. The application will run as this user.
useradd -m -d /home/pythonapp pythonapp

# pip from apt is out of date, so make it update itself and install virtualenv.
pip install --upgrade pip virtualenv

# Get the source code from the Google Cloud Repository
# git requires $HOME and it's not set during the startup script.
export HOME=/root
git config --global credential.helper gcloud.sh
git clone https://github.com/adamhajari/spyre.git /opt/app

# Install app dependencies
virtualenv /opt/app/spyre/tutorial/google_cloud/env
/opt/app/spyre/tutorial/google_cloud/env/bin/pip install -r /opt/app/spyre/tutorial/google_cloud/requirements.txt

# Make sure the pythonapp user owns the application code
chown -R pythonapp:pythonapp /opt/app

# Configure supervisor to start gunicorn inside of our virtualenv and run the
# application.
cat >/etc/supervisor/conf.d/python-app.conf << EOF
[program:spyreexample]
directory=/opt/app/spyre/tutorial/google_cloud
command=/opt/app/spyre/tutorial/google_cloud/env/bin/python2.7 /opt/app/spyre/tutorial/google_cloud/app.py
autostart=true
autorestart=true
user=pythonapp
# Environment variables ensure that the application runs inside of the
# configured virtualenv.
environment=VIRTUAL_ENV="/opt/app/spyre/tutorial/google_cloud/env/",PATH="/opt/app/spyre/tutorial/google_cloud/env/bin",\
    HOME="/home/pythonapp",USER="pythonapp"
stdout_logfile=syslog
stderr_logfile=syslog
EOF

supervisorctl reread
supervisorctl update

# Application should now be running under supervisor
# [END startup]


# wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh;
# bash miniconda.sh -b -p /home/pythonapp/miniconda
# export PATH="/home/pythonapp/miniconda/bin:$PATH"
# hash -r
# conda config --set always_yes yes --set changeps1 no
# conda update -q conda
# conda info -a
# conda create -q -n test-environment python=$TRAVIS_PYTHON_VERSION numpy matplotlib pandas
# source activate test-environment
# pip install flake8
# python setup.py install
# pip install --upgrade six