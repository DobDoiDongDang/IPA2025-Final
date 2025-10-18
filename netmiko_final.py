from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.61"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        int_list = []
        for interface in result:
            if interface["interface"].startswith("Gigabit"):
                status = interface["status"]
                int_list.append(f"{interface['interface']} {status}")
                if status == "up":
                    up += 1
                elif status == "down":
                    down += 1
                elif status == "administratively down":
                    admin_down += 1
        ans = ", ".join(int_list) + f" -> {up} up, {down}  down, {admin_down} administratively down"
        return ans

if __name__ == "__main__":
    print(gigabit_status())
