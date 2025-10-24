#######################################################################################
# Yourname:
# Your student ID: 66070225
# Your GitHub Repo: https://github.com/DobDoiDongDang/IPA2024-Final.git

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import requests, os, time, json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import restconf_final as restconf
import netconf_final as netconf
from netmiko_final import gigabit_status, check_motd
from ansible_final import showrun, config_motd

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.getenv("access_token")

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = os.getenv("room_id")
iplist = ["10.0.15.61", "10.0.15.62", "10.0.15.63", "10.0.15.64", "10.0.15.65"]
method = ""

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": f"Bearer {ACCESS_TOKEN}" }

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    command = ""
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/66070225"):
        
        methodorip = message.split()[1]

# 5. Complete the logic for each command
        if methodorip in iplist:
            command = message.split()[2]
            ip = methodorip
            if command == "motd":
                if len(message.split()) > 3:
                    result = config_motd(ip, "'"+" ".join(message.split()[3:])+"'")
                else:
                    result = check_motd(ip)
            elif method == "":
                result = "Error: No method specified"
            else:
                print(command)
                if command == "create":
                    if method == "restconf":
                        result = restconf.create(ip)
                    else:
                        result = netconf.create(ip)
                elif command == "status":
                    if method == "restconf":
                        result = restconf.status(ip)
                    else:
                        result = netconf.status(ip)
                elif command == "delete":
                    if method == "restconf":
                        result = restconf.delete(ip)
                    else:
                        result = netconf.delete(ip)
                elif command == "enable":
                    if method == "restconf":
                        result = restconf.enable(ip)
                    else:
                        result = netconf.enable(ip)
                elif command == "disable":
                    if method == "restconf":
                        result = restconf.disable(ip)
                    else:
                        result = netconf.disable(ip)
                elif command == "gigabit_status":
                        result = gigabit_status(ip)
                elif command == "showrun":
                    result = showrun(ip)
                else:
                    result = "Error: No command or unknown command"
        elif methodorip in ["restconf", "netconf"]:
            if methodorip == "restconf":
                result = "Ok: Restconf"
            else:
                result = "Ok: Netconf"
            method = methodorip 
        else:
            result = "Error: No IP specified"
        
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        if command == "showrun" and result == 'ok':
            filename = "show_run_66070225_CSR1kv.txt"
            fileobject = open(filename, "rb")
            filetype = "text/plain"
            postData = {
                "roomId": os.getenv('room_id'),
                "text": "show running config",
                "files": (filename, fileobject, filetype),
            }
            postData = MultipartEncoder(postData)
            HTTPHeaders = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": postData.content_type,
            }
        # other commands only send text, or no attached file.
        else:
            postData = {"roomId": os.getenv("room_id"), "text": result}
            postData = json.dumps(postData)

            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
            HTTPHeaders = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}   
        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=HTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
