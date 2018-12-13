"""

Functions used in program.py

"""

import os
import time

import requests
import boto3

from variables import *

def install_apache2(ssh, sftp, url):
	""" Install and configure apache2. """

	# Uptade the machine and install apache2
	in_, out_, err_ = ssh.exec_command("sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install apache2 -y")
	out_.channel.recv_exit_status()

	# Create the new apache configuration file
	if os.name == 'nt':
		os.system("echo. 2>Gen_Files/01-{}.conf".format(url))
	else:
		os.system("touch Gen_Files/01-{}.conf".format(url))

	# Create the new file with the good url
	vhost_non_conf = open('Ressources/vhost.conf','r')
	vhost_conf = open('Gen_Files/01-{}.conf'.format(url), 'w')

	line = 'not_empty'

	while line:
		line = vhost_non_conf.readline()
		vhost_conf.write(line.format(APACHE_LOG_DIR='{APACHE_LOG_DIR}', votre_url=url))

	vhost_conf.close()

	# Send the configuration file on the EC2 instance
	sftp.put('Gen_Files/01-{}.conf'.format(url), '/home/admin/01-{}.conf'.format(url))
	time.sleep(1)

	in_, out_, err_ = ssh.exec_command("sudo mv /home/admin/01-{}.conf /etc/apache2/sites-available/".format(url))
	out_.channel.recv_exit_status()
	in_, out_, err_ = ssh.exec_command("sudo mkdir /var/www/html/{}/".format(url))
	out_.channel.recv_exit_status()
	in_, out_, err_ = ssh.exec_command("sudo mv /var/www/html/index.html /var/www/html/{}".format(url))
	out_.channel.recv_exit_status()
	in_, out_, err_ = ssh.exec_command("sudo a2dissite 000-default")
	out_.channel.recv_exit_status()
	in_, out_, err_ = ssh.exec_command("sudo a2ensite 01-{}".format(url))
	out_.channel.recv_exit_status()
	in_, out_, err_ = ssh.exec_command("sudo systemctl reload apache2")
	out_.channel.recv_exit_status()

	print('Conf Apache OK.')

def install_php(ssh):
	""" Install and configure PHP. """

	in_, out_, err_ = ssh.exec_command("sudo apt-get install php-fpm -y")
	out_.channel.recv_exit_status()
	
	in_, out_, err_ = ssh.exec_command("sudo a2enmod proxy_fcgi setenvif")
	out_.channel.recv_exit_status()

	in_, out_, err_ = ssh.exec_command("sudo a2enconf php7.0-fpm")
	out_.channel.recv_exit_status()

	in_, out_, err_ = ssh.exec_command("sudo systemctl restart apache2")
	out_.channel.recv_exit_status()

	print('Conf PHP OK.')

def install_mysql(ssh, sftp):
	""" Install and configure MySQL. """

	in_, out_, err_ = ssh.exec_command("sudo apt-get install mysql-server -y && sudo apt-get install php7.0-mysql -y")
	out_.channel.recv_exit_status()

	# Create the new database installer file
	if os.name == 'nt':
		os.system("echo. 2>Gen_Files/bdd.sql")
	else:
		os.system("touch Gen_Files/bdd.sql")

	sql_non_conf = open('Ressources/bdd.txt', 'r')
	sql_conf = open('Gen_Files/bdd.sql', 'w')

	line = 'not_empty'

	while line:
		line = sql_non_conf.readline()
		sql_conf.write(line.format(db_name=WP_DB_NAME,db_user=WP_DB_USER,db_mdp=WP_DB_PASS,db_host=WP_DB_HOST))

	sql_conf.close()

	#Send the file on the EC2 instance
	sftp.put('Gen_Files/bdd.sql', '/home/admin/bdd.sql')
	time.sleep(1)

	print("Conf MySQL OK.")

def install_wp(ssh, sftp, url):
	""" Download and install WORDPRESS. """

	in_, out_, err_ = ssh.exec_command("sudo wget https://wordpress.org/latest.tar.gz -P /var/www/html/{}".format(url))
	out_.channel.recv_exit_status()
	in_, out_, err_ = ssh.exec_command("sudo tar zxvf /var/www/html/{}/latest.tar.gz -C /var/www/html/{}/".format(url, url))
	out_.channel.recv_exit_status()

	secret_key = 'https://api.wordpress.org/secret-key/1.1/salt/'
	r = requests.post(secret_key)

	if os.name == 'nt':
		os.system("echo. 2>Gen_Files/wp-config.php")
	else:
		os.system("touch Gen_Files/wp-config.php")

	wp_non_conf = open('Ressources/wp-config.txt', 'r')
	wp_conf = open('Gen_Files/wp-config.php', 'w')

	line = 'not_empty'

	while line:
		line = wp_non_conf.readline()
		wp_conf.write(line.format(db_name=WP_DB_NAME,db_user=WP_DB_USER,db_mdp=WP_DB_PASS,key_secret=r.text))

	wp_conf.close()

	# Send the config file on the EC2 instance
	sftp.put('Gen_Files/wp-config.php', '/home/admin/wp-config.php')
	time.sleep(1)

	in_, out_, err_ = ssh.exec_command("sudo mv /home/admin/wp-config.php /var/www/html/{}/wordpress/wp-config.php".format(url))
	out_.channel.recv_exit_status()

	in_, out_, err_ = ssh.exec_command("sudo mysql -u root < bdd.sql")
	out_.channel.recv_exit_status()

	# Delete the bdd.sql file because we don't need it anymore
	in_, out_, err_ = ssh.exec_command("rm bdd.sql")
	out_.channel.recv_exit_status()

	# Autorize Wordpress to write on the WP directory
	in_, out_, err_ = ssh.exec_command("sudo chown -R www-data:www-data /var/www/html/{}/wordpress/".format(url))
	out_.channel.recv_exit_status()

	print("Conf WP OK.")

def install_ssl(ssh, sftp, url, ip):
	""" Install a ssl certificate powered by let's encrypt. """

	print('Please add this IP : {} to your A record for the domain {}'.format(ip, url))

	caract = input('If you can\'t do that, please answer \'c\' otherwise answer anything : ') 

	if caract != 'c':
		#SSL
		in_, out_, err_ = ssh.exec_command("sudo apt-get install letsencrypt -y")
		out_.channel.recv_exit_status()
		in_, out_, err_ = ssh.exec_command("sudo systemctl stop apache2")
		out_.channel.recv_exit_status()
		in_, out_, err_ = ssh.exec_command("sudo letsencrypt certonly --standalone --agree-tos --email admin@{site} -d {site} -d www.{site} --standalone-supported-challenges http-01".format(site=url))
		out_.channel.recv_exit_status()

		vhost_ssl_non_conf = open('Ressources/vhost_ssl.conf','r')
		vhost_ssl_conf = open('Gen_Files/01-{}.conf'.format(url), 'w')

		line = 'not_empty'

		while line:
			line = vhost_ssl_non_conf.readline()
			vhost_ssl_conf.write(line.format(APACHE_LOG_DIR='{APACHE_LOG_DIR}', votre_url=url, HTTPS='{HTTPS}', SERVER_NAME='{SERVER_NAME}', REQUEST_URI='{REQUEST_URI}'))

		vhost_ssl_conf.close()	

		# Send the config file on the EC2 instance
		sftp.put('Gen_Files/01-{}.conf'.format(url), '/home/admin/01-{}.conf'.format(url))
		time.sleep(1)

		in_, out_, err_ = ssh.exec_command("sudo mv /home/admin/01-{}.conf /etc/apache2/sites-available/".format(url))
		out_.channel.recv_exit_status()
		in_, out_, err_ = ssh.exec_command("sudo systemctl start apache2")
		out_.channel.recv_exit_status()
		in_, out_, err_ = ssh.exec_command("sudo a2enmod ssl")
		out_.channel.recv_exit_status()
		in_, out_, err_ = ssh.exec_command("sudo a2enmod rewrite")
		out_.channel.recv_exit_status()
		in_, out_, err_ = ssh.exec_command("sudo systemctl restart apache2")
		out_.channel.recv_exit_status()

		print("Conf SSL OK.")

	else:
		print("Conf SSL NOT OK.")

def auto_renew_ssl(ssh, sftp, url):
	""" Create crontab job to automatically renew SSL certificate """

	# Install cron package
	in_, out_, err_ = ssh.exec_command("sudo apt-get install cron -y")
	out_.channel.recv_exit_status()

	# Create the new apache configuration file
	if os.name == 'nt':
		os.system("echo. 2>Gen_Files/renew_ssl.sh")
	else:
		os.system("touch Gen_Files/renew_ssl.sh")

	renew_ssl_non_conf = open('Ressources/renew_ssl.txt','r')
	renew_ssl_conf = open('Gen_Files/renew_ssl.sh', 'w')

	line = 'not_empty'

	while line:
		line = renew_ssl_non_conf.readline()
		renew_ssl_conf.write(line.format(site=url))

	renew_ssl_conf.close()	

	# Send the config file on the EC2 instance
	sftp.put('Gen_Files/renew_ssl.sh', '/home/admin/renew_ssl.sh')
	time.sleep(1)

	in_, out_, err_ = ssh.exec_command("sudo mv /home/admin/renew_ssl.sh /usr/sbin/renew_ssl.sh")
	out_.channel.recv_exit_status()

	in_, out_, err_ = ssh.exec_command("sudo sh -c \"echo \'0 0 1 * * root /usr/sbin/renew_ssl.sh\' >> /etc/crontab\"") 
	out_.channel.recv_exit_status()

def send_sms(message, number):
	""" Send a specific message to a specific number with Amazon SNS"""

	sms = boto3.client(
		"sns",
		aws_access_key_id = AWS_SNS_ACCESS_KEY,
		aws_secret_access_key = AWS_SNS_SECRET_KEY,
		region_name = AWS_SNS_REGION_NAME
	)

	# Send SMS
	sms.publish(PhoneNumber=number, Message=message)