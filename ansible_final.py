import subprocess
import os

os.environ['ANSIBLE_CONFIG'] = "./ansible.cfg"

def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', './ansible/ansible_playbook.yaml', '-i', './ansible/hosts']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=2' in result:
        return 'ok'
    else:
        return 'not ok ;-;'

def config_motd(ip, message):
    host = f"CSR1kv ansible_user=admin ansible_password=cisco ansible_host={ip} ansible_network_os=ios ansible_connection=network_cli"
    try:
        with open("./ansible/hosts", 'w') as f:
            f.write(host)
        command = ['ansible-playbook', './ansible/config_motd_playbook.yaml', '-i', './ansible/hosts', '-e', f'motd={message}']
        print(*command)
        result = subprocess.run(command, capture_output=True, text=True)
        result = result.stdout
        if 'ok=1' in result:
            return "Ok: success"
        else:
            return "Error: not success"
    except Exception as e:
       print("error :", e)

if __name__ == "__main__":
    print(config_motd("10.0.15.61", "'Authorized users only! Managed by 66070225'"))
