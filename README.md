# AutoInstallWPinAWS
Python script to automatically install Wordpress in a AWS EC2 instance
This script has only be tested on Debian ! 

## Requirements
To use this script you need to install Python3 and run it on an Linux machine
* On debian/ubuntu : `apt-get install python3`
* On centos : `yum install python3`

I currently develop a new version with Windows support.

Also you need to install pip3.
* On debian/ubuntu : `apt-get install pip3`
* On centos : `yum install pip3`

## Run the script
First, you need to create an Amazon AWS account.

Then, you have to create a key pair. Keep it name in mind. You'll need it in to run the program. (How to create a key pair on EC2 : https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)

After that, follow this tutorial : https://blog.ipswitch.com/how-to-create-an-ec2-instance-with-python

You'll need to follow theses parts :

* Create a User and get AWS Access ID and Secret Key
* Configure AWS Credentials Locally

When that was done, you have to edit the script `prg_aws.py` with your own informations.

Finally you can run the script by using : `python3 prg_aws.py`

## Informations

This script will create Amazon EC2 instance(s). Be carrefull, it can cost you money !
