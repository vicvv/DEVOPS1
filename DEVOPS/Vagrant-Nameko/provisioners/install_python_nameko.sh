
sudo apt -y update;
sudo apt -y install software-properties-common;
sudo add-apt-repository -y ppa:deadsnakes/ppa;
sudo apt -y update;
sudo apt -y install python3.7;
sudo apt -y update;
sudo apt -y install python3.7;
sudo apt -y install python3.7-dev;
sudo apt -y install python3.7-venv;
sudo wget https://bootstrap.pypa.io/get-pip.py;
sudo python3.7 get-pip.py;
sudo chown -R vagrant:vagrant /home/vagrant/.cache/pip;
sudo ln -s /usr/bin/python3.7 /usr/local/bin/python3;
sudo ln -s /usr/local/bin/pip /usr/local/bin/pip3;
sudo pip install nameko
sudo pip install psutil

# wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
# sudo dpkg -i erlang-solutions_1.0_all.deb
# sudo apt-get update
# sudo apt-get install erlang erlang-nox
# wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
# sudo apt-get update
# sudo apt-get install rabbitmq-server
# sudo update-rc.d rabbitmq-server defaults
# sudo service rabbitmq-server start
# sudo systemctl enable rabbitmq-server
# sudo systemctl start rabbitmq-server