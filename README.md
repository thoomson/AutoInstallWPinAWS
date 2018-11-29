# AutoInstallWPinAWS
Python script to automatically install Wordpress in an AWS EC2 instance
This script has only be tested on **Debian** and **Windows 10** ! Be carrefull when use it on others systems.

## Prepare your setup

To use this script you need to install Python3 and pip3.
* On debian/ubuntu : `apt-get install python3 pip3`
* On centos : `yum install python3 pip3`
* On Windows : install the last 3.X version on : https://www.python.org/downloads/

In the installation, be carrefull to select the option `Add Python to environnment variables`

![Python_Install](https://i.imgur.com/TMMV3nE.png)

After install Python3 and pip3, please install theses librairies : `boto3`, `paramiko` and `requests`.(`pip3 install boto3 paramiko requests` on your command line)

## AWS Preparation

To use this script, you need (obviously) an Amazon AWS account.

Then, you have to create a key pair. Keep it name in mind. You'll need it in to run the program. (How to create a key pair on EC2 : (https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) 

After that, you'll need to create a User and get AWS Access ID and Secret Key.
To do that :

1. Launch the Identity and Access Management console (IAM) in AWS. 

2. Click Users on the navigation menu on the left of the screen. 

3. In the popup window, click on Add User. 

![ipswitch.com](https://blog.ipswitch.com/hs-fs/hubfs/prateek-add-user-aws-iam.png?t=1543273056029&width=847&name=prateek-add-user-aws-iam.png)

4. In the new window, provide a user name and choose the 'Programmatic Access' access type, then click next. 

![ipswitch.com](https://blog.ipswitch.com/hs-fs/hubfs/prateek-add-user-aws-iam-2.png?t=1543273056029&width=831&name=prateek-add-user-aws-iam-2.png)

5. To set the permissions, choose 'Attach Existing Policies Directly' and in the Policy Filter type 'AmazonEC2FullAccess', you can choose any permission level, but in this example I'll click on the checkbox next to 'AmazonEC2FullAccess'. Then repeat this step with 'AmazonSNSFullAccess' and then click the 'next' button. 

![ipswitch.com](https://blog.ipswitch.com/hs-fs/hubfs/prateek-add-user-aws-iam-3.png?t=1543273056029&width=972&name=prateek-add-user-aws-iam-3.png)

6. Finally, review the user and permission levels, and click on the 'Create User' button. 

7. The next page will show your keys, as shown below. These are only available once, so it its a good idea to download and save then safely in a secure location. 

![ipswitch.com](https://blog.ipswitch.com/hs-fs/hubfs/prateek-add-user-aws-iam-4.png?t=1543273056029&width=985&name=prateek-add-user-aws-iam-4.png)

(credits to https://blog.ipswitch.com/how-to-create-an-ec2-instance-with-python for this tutorial and pictures)

## Run the script

When that was done, you have to edit the script `variables.py` with your own informations.

Finally you can run the script by using : `python3 program.py` or `python program.py` in Windows.

## Informations

This script will create Amazon EC2 instance(s). Be carrefull, it can cost you money !

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request