import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
# Testing on local environment so i use 192.168.86.146 (Lazy to use vpn)
api_url = "https://192.168.86.146/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070225"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
}
basicauth = ("admin", "cisco")


def create():
    yangConfig = {
            "ietf-interfaces:interface": {
            "name": "Loopback66070225",
            "description": "Ola",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.2.25.1",
                        "netmask": "255.255.255.0"
                    }
                ]}, 
            "ietf-ip:ipv6": {}
                }
            }
    resp = requests.put(api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code == 201):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070225 is created successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback 66070225"

def delete():
    resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
        <!!!REPLACEME with URL!!!>,
        auth=basicauth,
        headers=<!!!REPLACEME with HTTP Header!!!>,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "<!!!REPLACEME with proper message!!!>"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
