# ToDoApp

## Description

This is a small practice Flask project where users can create to do lists.

## Setup 

### Set Up Vagrant

The Vagrantfile included in this repository uses VirtualBox Hypervisor. If you wish to use a different Hypervisor please edit the Vagrantfile accordingly.

More info on how to setup Vagrant is available [here](https://developer.hashicorp.com/vagrant/docs).

1. `vagrant up` - Spins up VM.
1. `vagrant ssh` - SSH to VM.

### Securing The Server

These steps will help secure your server by reducing the attack service.

#### Disable root logins and password authentication.

1. In `/etc/ssh/sshd_config` - Set `PasswordAuthentication no`
1. In `/etc/ssh/sshd_config` - Set `PermitRootLogin no`
1. `sudo service ssh restart`

#### Set up UFW

This will block inbound connections on all ports other than those specified below.

1. `sudo apt-get install -y ufw`
1. `sudo ufw allow ssh`
1. `sudo ufw allow http`
1. `sudo ufw allow 443/tcp`
1. `sudo ufw --force enable`
1. `sudo ufw status`

### Installing Base Dependencies

1. `sudo apt-get -y update`
1. `sudo apt-get -y install python3 python3-venv python3-dev`
1. `sudo apt-get -y install supervisor nginx git`

### Installing The Application

1. `git clone https://github.com/Necas21/ToDoApp.git`
1. `cd ToDoApp`
1. `python3 -m venv .venv`
1. `source .venv/bin/activate`
1. `pip install -r requirements.txt`
1. `pip install gunicorn`

#### Create a .env file

This .env file will be used to load all of the environment variables required for the application to run.

Required environment variables:

1. SECRET_KEY
1. ADMIN_EMAIL
1. MAIL_SERVER
1. MAIL_PORT
1. MAIL_USERNAME
1. MAIL_PASSWORD

### Set up Gunicorn and Supervisor

1. `cp deployment/supervisor/todoapp.conf /etc/supervisor/conf.d/todoapp.conf`
1. `sudo supervisorctl reload`

The todoapp.conf file includes the Gunicorn command required to start the application.

### Set up Nginx

1. `mkdir certs`
1. `openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout certs/key.pem -out certs/cert.pem` - You can fill out the information required or just leave defaults.
1. `sudo rm /etc/nginx/sites-enabled/default`
1. `cp deployment/nginx/todoapp /etc/nginx/sites-enables/todoapp`
1. `sudo service nginx reload`


