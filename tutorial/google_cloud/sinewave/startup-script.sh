# [START startup]
set -v

GITHUB_REPO_URL="https://github.com/adamhajari/spyre.git"

# Install logging monitor. The monitor will automatically pickup logs sent to syslog.
curl -s "https://storage.googleapis.com/signals-agents/logging/google-fluentd-install.sh" | bash
service google-fluentd restart &

# Create a pythonapp user. The application will run as this user.
useradd -m -d /home/pythonapp pythonapp

# Install dependencies from apt
apt-get update
apt-get install -yq git build-essential supervisor libffi-dev libssl-dev

#Download and install the miniconda distribution of python
wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O /home/pythonapp/miniconda.sh;
bash /home/pythonapp/miniconda.sh -b -p /home/pythonapp/miniconda
chown -R pythonapp:pythonapp /home/pythonapp/miniconda/

# Get the source code from git
# git requires $HOME and it's not set during the startup script.
export HOME=/root
git clone $GITHUB_REPO_URL /opt/app

# create a virtualenv with the required scientific libraries
export PATH="/home/pythonapp/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a
conda create -q -n app-env python=2.7 numpy matplotlib pandas

# Install app dependencies
/home/pythonapp/miniconda/envs/app-env/bin/pip install -r /opt/app/tutorial/google_cloud/sinewave/requirements.txt

# Make sure the pythonapp user owns the application code
chown -R pythonapp:pythonapp /opt/app

# Configure supervisor to start gunicorn inside of our virtualenv and run the application.
cat >/etc/supervisor/conf.d/python-app.conf << EOF
[program:spyreexample]
directory=/opt/app/tutorial/google_cloud/sinewave
command=/home/pythonapp/miniconda/envs/app-env/bin/python2.7 /opt/app/tutorial/google_cloud/sinewave/sinewaveapp.py 0.0.0.0 8080
autostart=true
autorestart=true
user=pythonapp
# Environment variables ensure that the application runs inside of the configured virtualenv.
environment=VIRTUAL_ENV="/home/pythonapp/miniconda/envs/app-env/",PATH="/opt/app/tutorial/google_cloud/sinewave/env/bin",\
    HOME="/home/pythonapp",USER="root"
stdout_logfile=syslog
stderr_logfile=syslog
EOF

supervisorctl reread
supervisorctl update

# Application should now be running under supervisor
# [END startup]
