import ConfigParser
import requests
import json
import sys
import os

class SyncRackspace(object):

    def __init__(self):
        self.LIST_SERVERS_URI = '/servers/detail'
        self.username = None
        self.api_key = None
        self.token_request = None
        self.token = None
        self.server_info = []

    def make_it_so(self):
        self.get_config_info()
        self.get_auth_token()
        self.get_server_info()
        self.write_to_hosts()

    def get_config_info(self):
        # Read the rackspace api credentials from the connect.cfg file
        print "Reading the connect.cfg file..."

        config = ConfigParser.RawConfigParser()
        try:
            fp = open('connect.cfg')
        except IOError:
            print "Error: No 'connect.cfg' file found in current directory"
            sys.exit(1)

        config.readfp(fp)
        try:
            self.username = config.get('rackspace', 'username')
            self.api_key = config.get('rackspace', 'api_key')
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            print """
            There was an error processing the config file. Please make sure
            it has the following structure:
            
            [rackspace]
            username = <your_username>
            api_key = <your_api_key>
                  """
            sys.exit(1)

    def get_auth_token(self):
        print "Getting authentication token..."
        # Get AUTH-TOKEN
        token_url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
        payload = {"auth":{"RAX-KSKEY:apiKeyCredentials":
                  {"username":"%s" % self.username, "apiKey":"%s" % self.api_key}}}
        headers = {'content-type': 'application/json'}
        self.token_request = requests.post(token_url, data=json.dumps(payload), headers=headers)
        self.token = self.token_request.json()['access']['token']['id']

    def get_server_info(self):
        print "Getting server information..."
        # Get Server info for first generation
        headers = {"X-Auth-Token": "%s" % self.token}

        firstgen_server_api_url = None
        for server_dict in self.token_request.json()['access']['serviceCatalog']:
            if server_dict['name'] == 'cloudServers':
                firstgen_server_api_url = server_dict['endpoints'][0]['publicURL']
                break
        request = requests.get(firstgen_server_api_url + self.LIST_SERVERS_URI, 
                                        headers=headers)
        first_gen_json = request.json()

        # Get Server info for second generation servers
        secondgen_server_api_url = None
        for server_dict in self.token_request.json()['access']['serviceCatalog']:
            if server_dict['name'] == 'cloudServersOpenStack':
                secondgen_server_api_url = server_dict['endpoints'][0]['publicURL']
                break
        request = requests.get(secondgen_server_api_url + self.LIST_SERVERS_URI,
                                         headers=headers)
        second_gen_json = request.json()


        # Create list of all server names and ips
        for server in first_gen_json['servers']:
            self.server_info.append((server['name'], server['addresses']['public'][0]))
        for server in second_gen_json['servers']:
            self.server_info.append((server['name'], server['accessIPv4']))

    def write_to_hosts(self):
        print "Writing to hosts file..."
        # Get information from the ect/hosts file
        old_lines = []
        with open('/etc/hosts') as fp:
            for line in fp.readlines():
                # Check to see if the line is just a newline character
                try:
                    ip = line.split()[0]
                except IndexError:
                    old_lines.append(line)
                    continue
                for server in self.server_info:
                    if server[0] == ip:
                        # If the ip address is already in the hosts file, and it has the alias from
                        # rackspace associated with it, remove the ip/alias info from the server_info
                        # lise and continue
                        if server[1] in line.split():
                            self.server_info.pop(self.server_info.index(server))
                            continue
                        # If it doesn't have the alias from rackspace associated with it, add that name
                        else:
                            line = line + " %s" % server[1]
                            old_lines.append(line)
                            continue
                else:
                    old_lines.append(line)

        # Write to a temporary file
        with open ('/tmp/new_hosts.tmp', 'wb') as fp:
            for line in self.server_info:
                fp.write('%s\t%s\n' % (line[0], line[1]))
            for line in old_lines:
                fp.write(line)

        # Overwrite the /etc/hosts file with the new information
        os.system('sudo mv /tmp/new_hosts.tmp /etc/hosts')
        print "Success!"

if __name__ == "__main__":
    sync = SyncRackspace()
    sync.make_it_so()