"""

Install and configure Wordpress on an Amazon AWS EC2 instance.
Used Apache2, PHP 7.0, MySQL and Let's encrypt (SSL is optionnal)

"""

# Libraries
import time

import boto3
import paramiko

from functions import *
from variables import *

# Beginning of the program
url = input('Enter the URL as \'example.com\' (without \'www\' or \'http(s)\'): ')

ssl = input('Do you want an HTTPS website ? (o/n): ').lower() # HTTPS is powered by LetsEncrypt

# Create the boto3 ressource
ec2 = boto3.resource(
	'ec2', 
	aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_KEY,
    region_name = AWS_REGION_NAME
 )

# Create a new EC2 instance
instances = ec2.create_instances(
    ImageId = AWS_AMI_ID,
    MinCount = 1,
    MaxCount = 1,
    InstanceType = AWS_INSTANCE,
    KeyName = AWS_KEY_NAME
 )

instance = instances[0]

print("Please wait until the installation..")

# Wait for the instance to enter the running state
instance.wait_until_running()

# Reload the instance attributes
instance.load()

# Save the ip of the instance
ip = instance.public_ip_address

# Wait a bit for the instance's initialisation
time.sleep(4)

# SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(str(ip), username='admin', key_filename=AWS_KEY_FILENAME)
sftp = ssh.open_sftp()

# Install and configure Apache2
install_apache2(ssh, sftp, url)

# Install SSL certificate if desired
if ssl == 'o':
	install_ssl(ssh, sftp, url, ip)
	auto_renew_ssl(ssh, sftp, url)

# Install and configure PHP
install_php(ssh)

# Install and configure MySQL
install_mysql(ssh, sftp)

# Pre-install Wordpress
install_wp(ssh, sftp, url)

# End of the SSH connection
ssh.close()

print('IP of your machine : ' + ip)# Display the public IP of the AWS instance
print('The installation is finished !')

# Send SMS
message = "Your Wordpress site on EC2 is installed ! Go to it on : {} ({})".format(url, ip)
send_sms(message, YOUR_PHONE_NUMBER)

# End of the program