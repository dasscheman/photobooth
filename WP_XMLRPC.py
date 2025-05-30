import urllib
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import xmlrpclib
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import os
########################### Read Me First ###############################
'''
------------------------------------------In DETAIL--------------------------------
Description
===========
Add new posts to WordPress remotely using Python using XMLRPC library provided by the WordPress.
Installation Requirement
************************
Verify you meet the following requirements
==========================================
Install Python 2.7 (Don't download 3+, as most libraries dont yet support version 3). 
Install from PyPI using easy_install python-wordpress-xmlrpc 
Easy_Install Link: https://pypi.python.org/pypi/setuptools
==========================================
Windows Installation Guide
==========================
-Download and Install Easy_Install from above Link -Extract Downloaded File and from CMD go to the extracted directory and run 'python setup.py install'. This will install easy_install. -Go to %/python27/script and run following command easy_install python-wordpress-xmlrpc
Ubuntu Installation Guide
=========================
sudo apt-get install python-setuptools 
sudo easy_install python-wordpress-xmlrpc
Note: Script has its dummy data to work initially which you can change or integrate with your code easily for making it more dynamic.
****************************************
For Bugs/Suggestions
contact@waqasjamal.com
****************************************
------------------------------------------In DETAIL--------------------------------		
'''
class Custom_WP_XMLRPC:
    def post_article(self, wpUrl, wpUserName, wpPassword, PhotoName, PhotoPath):
        self.wpUrl=wpUrl
        self.wpUserName=wpUserName
        self.wpPassword=wpPassword
        
        #Upload to WordPress
        client = Client(self.wpUrl,self.wpUserName,self.wpPassword)
        filename = PhotoPath +  PhotoName
        # prepare metadata
        data = {'name': PhotoName,'type': 'image/gif',}

        # read the binary file and let the XMLRPC library encode it into base64
        with open(filename, 'rb') as img:
                data['bits'] = xmlrpc_client.Binary(img.read())
        response = client.call(media.UploadFile(data))
        print('Post Successfully posted. Its Id is: ',response['id'])



