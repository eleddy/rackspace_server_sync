import ConfigParser
import requests
import json
import sys

LIST_SERVERS_URI = '/servers/detail'

# Read the rackspace api credentials form the connect.cfg file
config = ConfigParser.RawConfigParser()
try:
    fp = open('connect.cfg')
except IOError:
    print "Error: No 'connect.cfg' file found in current directory"
    sys.exit(1)

config.readfp(fp)
try:
    username = config.get('rackspace', 'username')
    api_key = config.get('rackspace', 'api_key')
except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
    print """
    There was an error processing the config file. Please make sure
    it has the following structure:
    
    [rackspace]
    username = <your_username>
    api_key = <your_api_key>
          """
    sys.exit(1)

# Get AUTH-TOKEN
token_url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
payload = {"auth":{"RAX-KSKEY:apiKeyCredentials":{"username":"%s" % username, "apiKey":"%s" % api_key}}}
headers = {'content-type': 'application/json'}
request = requests.post(token_url, data=json.dumps(payload), headers=headers)
token = request.json()['access']['token']['id']

# Get Server info for first generation
firstgen_server_api_url = None
for server_dict in request.json()['access']['serviceCatalog']:
    if server_dict['name'] == 'cloudServers':
        firstgen_server_api_url = server_dict['endpoints'][0]['publicURL']
        break

headers = {"X-Auth-Token": "%s" % token}
firstgen_request = requests.get(firstgen_server_api_url + LIST_SERVERS_URI, headers=headers)
first_gen_json = firstgen_request.json()

# Get Server info for second generation servers
secondgen_server_api_url = None
for server_dict in request.json()['access']['serviceCatalog']:
    if server_dict['name'] == 'cloudServersOpenStack':
        secondgen_server_api_url = server_dict['endpoints'][0]['publicURL']
        break

headers = {"X-Auth-Token": "%s" % token}
secondgen_request = requests.get(secondgen_server_api_url + LIST_SERVERS_URI, headers=headers)
second_gen_json = secondgen_request.json()

# Create list of all server names and ips
server_info = []
for server in first_gen_json['servers']:
    server_info.append(server['name'], ['server']['addresses']['public'][0])


import pdb; pdb.set_trace()
x['servers'][0]['name']
x['servers'][0]['addresses']['public'][0]


print "FIRST GEN SERVERS"
print "=" * 80
print first_gen_json

print '\n' * 2

print 'SECOND GEN SERVERS'
print "=" * 80
print second_gen_json