#!/usr/bin/python

import os
import re
import sys
from jinja2 import Template
import platform
import argparse

parser = argparse.ArgumentParser(description='Generate filezilla formatted xml from virtualmin')

parser.add_argument('-p', '--port', default=22, help="the port to use")
parser.add_argument('-t', '--protocol', default=0, help="the protocol to use: ftp - 0, sftp - 1")

args = vars(parser.parse_args())

port = args['port']
protocol = args['protocol']


hostname = platform.node()

virtualmin_dir = "/etc/webmin/virtual-server/domains/"

sites = []
for filename in os.listdir(virtualmin_dir):
	file = open(virtualmin_dir + filename, "r")
	domain = ""
	user = ""
	password = ""
	for line in file:
		dom_result = re.search("^dom=(.*)$",line)
		if(dom_result):
			domain = dom_result.group(1)
		user_result = re.search("^user=(.*)$",line)
		if(user_result):
			user = user_result.group(1)
		pass_result = re.search("^pass=(.*)$",line)
		if(pass_result):
			password = pass_result.group(1)
	sites.append({'domain':domain,'user':user,'password':password})

tmpl = Template(u'''\
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<FileZilla3>
    <Servers>
        <Folder>{{folder}}
    	{%- for site in sites %}
            <Server>
                <Host>{{site.domain}}</Host>
                <Port>{{port}}</Port>
                <Protocol>{{protocol}}</Protocol>
                <Type>0</Type>
                <User>{{site.user}}</User>
                <Pass>{{ site.password }}</Pass>
                <Logontype>1</Logontype>
                <TimezoneOffset>0</TimezoneOffset>
                <PasvMode>MODE_DEFAULT</PasvMode>
                <MaximumMultipleConnections>0</MaximumMultipleConnections>
                <EncodingType>Auto</EncodingType>
                <BypassProxy>0</BypassProxy>
                <Name>{{site.domain}}</Name>
                <Comments></Comments>
                <LocalDir></LocalDir>
                <RemoteDir></RemoteDir>
                <SyncBrowsing>0</SyncBrowsing>{{site.domain}}
            </Server>
    	{%- endfor %}
        </Folder>
    </Servers>
</FileZilla3>
''')

print tmpl.render( sites = sites, folder = hostname+"-server", port = port, protocol = protocol )
