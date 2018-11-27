"""

Variables used in prg_aws.py and functions.py.
Edit them with your own informations.

"""

# Wordpress
WP_DB_HOST = 'localhost'
WP_DB_NAME = 'wp_database'
WP_DB_USER = 'wp_user'
WP_DB_PASS = 'wikipass' 

#AWS
AWS_KEY_NAME = 'MaPaire'
AWS_INSTANCE = 't3.nano'
AWS_AMI_ID = 'ami-05829248ffee66250' #Note: The program was developped for Debian 9
AWS_ACCESS_KEY = 'YOUR_ACCESS_KEY'
AWS_SECRET_KEY = 'YOUR_SECRET_KEY'
AWS_REGION_NAME = 'us-east-2'
AWS_KEY_FILENAME = '/directory/to/your/key/MaKey.pem'

#SMS
AWS_SNS_ACCESS_KEY = AWS_ACCESS_KEY
AWS_SNS_SECRET_KEY = AWS_SECRET_KEY
YOUR_PHONE_NUMBER = '+00XXXXXXXXX'
AWS_SNS_REGION_NAME = 'us-east-1' #Supported regions : https://docs.aws.amazon.com/en_us/sns/latest/dg/sms_supported-countries.html