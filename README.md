Setup Steps

1. Install virtual environment `pip3 install virtualenv`
2. Create virtual environment `virtualenv venv --python=python3`
3. Activate virtual environment `source venv/bin/activate`

4. (optional) Leave virtual environment `deactivate`
5. Install Flask-RESTful library 'pip install Flask-Restful'

Deploy to AWS EC2 instance

## Deploy to AWS

If deploying on AWS, after installing Ubuntu 16.04, make sure to install libpcre3 and libpcre3-dev by running the following commands:

```bash
sudo apt-get install libpcre3 libpcre3-dev
pip install uwsgi -I --no-cache-dir
```

## Install PostreSQL on Ubuntu 16.04

While logged in as root user:

```bash
apt-get update
apt-get install postgresql postgresql-contrib
```

After installation, change user to postgres user by running

```bash
sudo -i -u postgres
```

Connect to the database by running

```bash
psql
```

To exit postgres database console, run

```bash
\q
```

To exit postgres user

```bash
exit
```

## Create a user in Ubuntu 16.04

To create a new user, run the following command and enter the user details as prompted (password, full name etc). Remember to replace "jose" with the name of your user.

```bash
adduser jose
```

### Add the new user to sudo users

Running the visudo command will open a file (normally located at /etc/sudoers).

```bash
visudo
```

Under "User privilege specification", add the following line below root line

```bash
jose ALL=(ALL:ALL) ALL
```

Save the file with CNTR+O and press enter to save it. Then CNTR+X to exit the file.

### To enable logging in to the server as the newly created user, enable password login to the server by running

```bash
vi /etc/ssh/sshd_config
```

This opens another file. To disable root login with password, change the following line. Note you need to press "i" key to go to insert/edit mode before changing the contents of the file.

```bash
PermitRootLogin yes
```

to

```bash
PermitRootLogin no
```

Scroll down to the end of the file and add the following line

```bash
AllowUsers jose
```

To exit edit/insert mode, press escape key then ":" followed by wq and press enter. "wq" writes the file to disc and quits the file.

Finally, run

```bash
service sshd reload
```

## Set up New User with PostgreSQL Permissions

This section assumes you created a new unix user in Ubuntu 16.04 (instructions in the previous lecture) and you are logged into the server as the new user.

To become the postgres user, run

```bash
sudo su
sudo -i -u postgres
```

To create a postgres user, run the following command. Note, the user must have the same name as the unix user logged into the server ("jose" in our case).

```bash
createuser jose -P
```

You will prompted twice to set the password for the new postgres user.

To create a database, run

```bash
createdb jose
```

To enforce password login to PostgreSQL with user jose, run the following commands. Note 9.5 is the PostgreSQL version installed in your server. Later this version may change so make sure to change your accordingly.

```bash
vi /etc/postgresql/9.5/main/pg_hba.conf
```

Scroll down to the bottom and change "peer" to "md5" in the following line under '# "local" is for unix domain socket connections only comment'. This is how the line should look after changing.

```bash
local all all md5
```

Finally, write and quit.

## Setting up Nginx

To install and cofigure Nginx on your server, follow the following instructions.

First, you need to update your server by running

```bash
sudo apt-get update
```

To install Nginx, run

```bash
sudo apt-get install nginx
```

Allow Nginx access through firewall (otherwise incoming requests will be blocked by the firewall)

```bash
sudo ufw enable
sudo ufw allow 'Nginx HTTP'
```

Also since we have enabled firewall, remember to allow ssh through the firewall, else you will get locked out of the server.

```bash
sudo ufw allow ssh
```

You can check firewall status by using

```bash
sudo ufw status
```

To check Nginx status, use

```bash
systemctl status nginx
```

The following commands stop, start and restart Nginx respectively.

```bash
systemctl stop nginx
systemctl start nginx
systemctl restart nginx
```

### Configuring Nginx

Create a new file for the items REST API configuration.

```bash
sudo vi /etc/nginx/sites-available/items-rest.conf
```

Press "i" key (insert mode), copy and paste the following to the file

```bash
server {
	listen 80;
	real_ip_header X-Forwarded-For;
	set_real_ip_from 127.0.0.1;
	server_name localhost;

	location / {
		include uwsgi_params;
		uwsgi_pass unix:/var/www/html/items-rest/socket.sock;
		uwsgi_modifier1 30;
	}

	error_page 404 /404.html;
	location = 404.html {
		root /usr/share/nginx/html;
	}

	error_page 500 502  503 504 50x.html;
	location = /50x.html {
		root /usr/share/nginx/html;
	}
}
```

After writing and quiting the file (escape key then :wq enter) enable the configuration by running

```bash
sudo ln -s /etc/nginx/sites-available/items-rest.conf /etc/nginx/sites-enabled/
```

### Create the socket.sock file and clone the items rest app

Create a directory/folder for the app

```bash
sudo mkdir /var/www/html/items-rest
```

Since the director was created with root user, give access to the unix user ("jose" in our case) by making the user the owner of the directory.

```bash
sudo chown jose:jose /var/www/html/items-rest
```

Got to the directory, clone the app and install dependencies. Run the following commands one by one in that order.

```bash
cd /var/www/html/items-rest
git clone https://github.com/schoolofcode-me/stores-rest-api.git .
mkdir log
sudo apt-get install python-pip python3-dev libpq-dev
pip install virtualenv
virtualenv venv --python=python3.5
source venv/bin/activate
pip install -r requirements.txt
```

## Setting up uWSGI

This guide will help you set up uWSGI on your server to run the items rest app. Go to the items-rest directory we created in the previous lecture.

```bash
cd /var/www/html/items-rest
```

### Create Ubuntu service

Run the following command to create a service file.

```bash
sudo vi /etc/systemd/system/uwsgi_items_rest.service
```

Copy and paste the following to the file. Note "jose:1234" is the username:password combination of the Postgres user we created before. Change yours accordingly.

```bash
[Unit]
Description=uWSGI items rest

[Service]
Environment=DATABASE_URL=postgres://jose:1234@localhost:5432/jose
ExecStart=/var/www/html/items-rest/venv/bin/uwsgi --master --emperor /var/www/html/items-rest/uwsgi.ini --die-on-term --uid jose --gid jose --logto /var/www/html/items-rest/log/emperor.log
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

Replace the uwsgi.ini file contents with the following

```bash
[uwsgi]
base = /var/www/html/items-rest
app = run
module = %(app)

home = %(base)/venv
pythonpath = %(base)

socket = %(base)/socket.sock

chmod-socket = 777

processes = 8

threads = 8

harakiri = 15

callable = app

logto = /var/www/html/items-rest/log/%n.log
```

Finally start the app by running

```bash
sudo systemctl start uwsgi_items_rest
```
