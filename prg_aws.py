#Libraries
import os
import time
from functions import *
from variables import *

try:
	import boto3
except ModuleNotFoundError:
	os.system('pip3 install boto3')
	import boto3

try:
	import paramiko
except ModuleNotFoundError:
	os.system('pip3 install paramiko')
	import paramiko

#Pre-start
os.system("rm -r Gen_Files/*")

#Beginning of the program
url = input('Enter the URL as \'example.com\' (without \'www\' or \'http(s)\'): ')

ssl = input('Do you want an HTTPS website ? (o/n): ').lower() # HTTPS is powered by LetsEncrypt

if ssl != 'o':
	ssl = 'n'

#Create the boto3 ressource
ec2 = boto3.resource(
	'ec2', 
	aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name =AWS_REGION_NAME
    )

# Create a new EC2 instance
instances = ec2.create_instances(
    ImageId=AWS_AMI_ID,
    MinCount=1,
    MaxCount=1,
    InstanceType=AWS_INSTANCE,
    KeyName='MaPaire'
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
time.sleep(5)

# SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(str(ip), username='admin', key_filename='/home/user/Bureau/OS/MaPaire.pem')
sftp = ssh.open_sftp()

# APACHE
install_apache2(ssh, sftp, url)

#SSL
if ssl == 'o':
	install_ssl(ssh, sftp, url, ip)

# PHP
install_php(ssh)

# MYSQL
install_mysql(ssh, sftp)

# WORDPRESS
install_wp(ssh, sftp, url)

# End of the SSH connection
ssh.close()

print('IP of your machine : ' + ip)# Display the public IP of the AWS instance
print('Please note that this is the password for the wordpress database: ' + WP_DB_PASS)# Display the BDD password. Please note it.

# End of the program