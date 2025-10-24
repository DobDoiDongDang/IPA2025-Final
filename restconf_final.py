import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
}
basicauth = ("admin", "cisco")

def status(ip):
    api_url_status = f"https://{ip}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070225"

    resp = requests.get(
        api_url_status,
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070225 is enabled (checked by Restconf)"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070225 is disabled (checked by Restconf)"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 66070225 (checked by Restconf)"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))

def create(ip):
    api_url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070225"
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
        return "Cannot create: Interface loopback 66070225 (checked by Restconf)"

def delete(ip):
    api_url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070225"
    resp = requests.delete(
        api_url,
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070225 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 66070225 (checked by Restconf)"

def enable(ip):
    api_url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070225"
    if "enabled" in status(ip):
        return "Cannot enable: Interface loopback 66070225 (checked by Restconf)"
    yangConfig = {
            "ietf-interfaces:interface": {
            "name": "Loopback66070225",
            "description": "Ola",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True, 
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
    resp = requests.put(
        api_url,
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070225 is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 66070225 (checked by Restconf)"

def disable(ip):
    api_url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070225"
    if "disabled" in status(ip):
        return "Cannot disable: Interface loopback 66070225 (checked by Restconf)"
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
    resp = requests.put(
        api_url,
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070225 is disabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot disabled: Interface loopback 66070225 (checked by Restconf)"
if __name__ == "__main__":
    print(create("10.0.15.61"))
