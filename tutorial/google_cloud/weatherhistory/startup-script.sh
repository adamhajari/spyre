# [START startup]
set -v

GITHUB_REPO_URL="https://github.com/adamhajari/spyre.git"
USER=adamhajari

# Install logging monitor. The monitor will automatically pickup logs sent to syslog.
curl -s "https://storage.googleapis.com/signals-agents/logging/google-fluentd-install.sh" | bash
service google-fluentd restart &

# Install dependencies from apt
apt-get update
apt-get install -yq git build-essential supervisor libffi-dev libssl-dev

#Download and install the miniconda distribution of python
wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O /home/$USER/miniconda.sh;
bash /home/$USER/miniconda.sh -b -p /home/$USER/miniconda

# Get the source code from git
# git requires $HOME and it's not set during the startup script.

export HOME=/home/$USER/
git clone $GITHUB_REPO_URL /home/$USER/spyre/

# create a virtualenv with the required scientific libraries
export PATH="/home/$USER/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a
conda create -q -n app-env python=2.7 pandas==0.21.0 numpy==1.11.1 matplotlib==2.1.0 

# Install app dependencies
/home/$USER/miniconda/envs/app-env/bin/pip install -r /home/$USER/spyre/tutorial/google_cloud/weatherhistory/requirements.txt

