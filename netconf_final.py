from ncclient import manager
import xmltodict

def status(ip):
    m = manager.connect(
        host=f"{ip}",
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
    )
    netconf_filter = """
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070225</name>
                <admin-status/>
                <oper-status/>
            </interface>
        </interfaces-state>
    </filter>
    """

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        if netconf_reply_dict['rpc-reply']['data']:
            # extract admin_status and oper_status from netconf_reply_dict
            reply = netconf_reply_dict['rpc-reply']
            print(reply['data']['interfaces-state'])
            admin_status = reply['data']['interfaces-state']['interface']['admin-status']
            oper_status = reply['data']['interfaces-state']['interface']['oper-status']
            if admin_status == 'up' and oper_status == 'up':
                return "Interface loopback 66070225 is enabled (checked by Netconf)"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback 66070225 is disabled (checked by Netconf)"
        else: # no operation-state data
            return "No Interface loopback 66070225 (checked by Netconf)"
    except Exception as e:
        print(f"Error! : {e}")

def create(ip):
    if "is" in status(ip):
        return "Cannot create: Interface loopback 66070225"
    m = manager.connect(
        host=f"{ip}",
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
    )
    netconf_loopback = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"
              xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
            <interface>
                <name>Loopback66070225</name>
                <type>ianaift:softwareLoopback</type>
                <enabled>false</enabled>
            </interface>
        </interfaces>
    </config>
    """


    try:
        netconf_reply = netconf_edit_config(m, netconf_loopback)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070225 is created successfully using Netconf"
        else:
            return "Cannot create: Interface loopback 66070225"
    except Exception as e:
        print("Error! :", e)


def delete(ip):
    m = manager.connect(
        host=f"{ip}",
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
    )
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interface nc:operation="delete">
                <name>Loopback66070225</name>
            </interface>
        </interfaces>
    </config>"""

    try:
        netconf_reply = netconf_edit_config(m, netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070225 is deleted successfully using Netconf"
        else:
            return "Cannot delete: Interface loopback 66070123"
    except:
        print("Error!")


def enable(ip):
    if "enabled" in status(ip):
        return "Cannot enable: Interface loopback 66070225 (checked by Netconf)"
    m = manager.connect(
        host=f"{ip}",
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
    )
    netconf_config = """
    <config>
         <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"
              xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
            <interface>
                <name>Loopback66070225</name>
                    <type>ianaift:softwareLoopback</type>
                    <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>

    """

    try:
        netconf_reply = netconf_edit_config(m, netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070225 is enabled successfully using Netconf"
        else:
            return "Cannot enable: Interface loopback 66070225 (checked by Netconf)"
    except Exception as e:
        print("Error! :", e)


def disable(ip):
    if "disabled" in status(ip):
        return "Cannot shutdown: Interface loopback 66070225 (checked by Netconf)"
    m = manager.connect(
        host=f"{ip}",
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
    )
    netconf_config = """
    <config>
         <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"
              xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
            <interface>
                <name>Loopback66070225</name>
                    <type>ianaift:softwareLoopback</type>
                    <enabled>false</enabled>
            </interface>
        </interfaces>
    </config>
    """
    try:
        netconf_reply = netconf_edit_config(m, netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070123 is shutdowned successfully using Netconf"
        else:
            return "Cannot shutdown: Interface loopback 66070123 (checked by Netconf)"
    except Exception as e:
        print("Error! :", e)

def netconf_edit_config(m, netconf_config):
    return  m.edit_config(target="running", config=netconf_config)

if __name__ == "__main__":
    print(delete("10.0.15.61"))
