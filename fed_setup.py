#/usr/bin/env python
#
# Checks if node.js is installed, and installs it if needed. Then installs npm and gem packages for FED dev environments.
#
# Brian LaShomb, @lashomb

# Installs pip if needed.
import os
from pprint import pprint
from subprocess import call

installed = {}
pip_path = "/usr/local/bin/pip"
gem_path = "/usr/bin/gem"
node_url = "http://nodejs.org/dist/v0.12.4/node-v0.12.4.pkg"
wkhtmltopdf_url = "http://iweb.dl.sourceforge.net/project/wkhtmltopdf/0.12.2.1/wkhtmltox-0.12.2.1_osx-cocoa-x86-64.pkg"

if not os.path.exists(pip_path):
    call(["/usr/bin/easy_install", "pip"])
    installed['pip: ']='installed'
else:
    installed['pip: ']='failed'


# Installs the python module Requests.
if os.path.exists(pip_path):
    call([pip_path, "install", "requests"])
    installed['requests: ']='installed'
else:
    installed['requests: ']='failed'
    exit(1)

####

import requests
node_path = "/usr/local/bin/node"
wkhtmltopdf_path = "/usr/local/bin/wkhtmltopdf"
npm_path = "/usr/local/bin/npm"
grunt_path = "/usr/local/bin/grunt"
gem_list = ["casperjs", "fuelsdk", "nokogiri", "jasmine", "phantomjs", "premailer", "compass", "bootstrap-sass", "sass-json-vars"]

# Temp directory in /Users/Shared
os.chdir("/Users/Shared")

# Download method for pkg installers.
def download_file(url):
    pkg_name = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(pkg_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return pkg_name

# Download the pkgs
node_package = os.path.realpath(download_file(node_url))
wkhtmltopdf_package = os.path.realpath(download_file(wkhtmltopdf_url))


####

# Installing node.js
if not os.path.exists(node_path):
    call(["/usr/sbin/installer", "-pkg", node_package, "-target", "/"])
    installed['nodejs: ']='installed'

# Installing wkhtmltopdf
if not os.path.exists(wkhtmltopdf_path):
    call(["/usr/sbin/installer", "-pkg", wkhtmltopdf_package, "-target", "/"])
    installed['wkhtmltopdf: ']='installed'

# Calling NPM to install Grunt
if os.path.exists(npm_path):
    call(["npm", "install", "grunt"])
    installed['grunt: ']='installed'
else:
    installed['grunt: ']='failed'
    exit(1)


# Calling NPM to install Grunt CLI
if os.path.exists(npm_path):
    call(["npm", "install", "-g", "grunt-cli"])
    installed['grunt-cli: ']='installed'
else:
    installed['grunt-cli: ']='failed'
    exit(1)

# Installing rubygems
for gem in gem_list:
    if os.path.exists(gem_path):
        call(["gem", "install", gem])
        installed['%s: ' % gem]='installed'
    else:
        installed['%s: ' % gem]='failed'
        exit(1)

pprint(installed)
