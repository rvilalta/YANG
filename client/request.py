import requests 
import json
import time

INTRUSION_DETECTION_URL='http://127.0.0.1:8080/restconf/config/intrusiondetection/'
ALARM_SERVER_URL='http://127.0.0.1:8081/restconf/operations/triggerAlarm/'

#ARM system
status={'systemStatus':'armed'}
r = requests.put(INTRUSION_DETECTION_URL, headers={'Content-type':'application/json'}, data=json.dumps(status) )
print r.text

while True:
    r = requests.get(INTRUSION_DETECTION_URL)
    response= json.loads(r.text)
    if response['sensors']['status'] == 'occupied' :
        r = requests.post(ALARM_SERVER_URL)
        print 'Ocuppied!'
        time.sleep(1)    

