from time import sleep
import os
import json
import requests

def send_log_to_teams(webhook, log):
    card_payload = { 
        "type":"message",
        "attachments":[
            {
                "contentType":"application/vnd.microsoft.card.adaptive",
                "contentUrl":None,
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": f"New Log by {log['node_id']}"
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {
                                    "title": "Log Time (UTC)",
                                    "value": log["utc_time"]
                                },
                                {
                                    "title": "Source (IP:Port)",
                                    "value": f"{log.get('src_host', 'UNKNOWN')}:{log.get('src_port', 'UNKNOWN')}"
                                },
                                {
                                    "title": "Destination (IP:Port)",
                                    "value": f"{log.get('dst_host', 'UNKNOWN')}:{log.get('dst_port', 'UNKNOWN')}"
                                },
                                {
                                    "title": "Logdata",
                                    "value": f"{str(log.get('logdata', 'UNKNOWN'))}"
                                }   
                            ]
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.6"
                }
            }
        
    ]}
    print("Sending Message")
    response = requests.post(webhook, json=card_payload)
    print(response.text)


required_keys = ['TEAMS_WEBHOOK']
canary_log_path = os.environ.get('CANARY_LOG_PATH', '/var/tmp/opencanary.log')
for key in required_keys:
    if key not in os.environ.keys():
        raise(KeyError(f"Required Env Var {key} not set."))
f = open(canary_log_path)
while True:
    l = f.readline()
    if l:
        try:
            line = json.loads(l)
            send_log_to_teams(os.environ['TEAMS_WEBHOOK'], line)
        except Exception as _:
            print(_)
    else:
        sleep(10) 