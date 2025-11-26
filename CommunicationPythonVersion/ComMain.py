from Boot import do_connect
from WifScanner import wifi_scan
from Subscribe import do_subscribe
from Publish import do_publish
WIFI_CREDENTIALS = {"SSID" : "",
                    "PASSWORD" : ""}

MQTT_CREDENTIALS = {"host": 172.0.1.0,
                    "port": 1883,
                    "client_id": "id",
                    "user": "user",
                    "password": "password"}

def conmutador(act_code,JSON):
    
    if(act_code == 0):
        wifi_connection = do_connect(WIFI_CREDENTIALS)
        return_value = wifi_connection
        if (wifi_connection == 0): #WIFI connection
            print("Connection failed")
        else:
            print("Connection established")
    if else(act_code ==1): #Wifi scan
        scan_wifi_json = wifi_scan(JSON)
        return_value = scan_wifi_json 
    if else(act_code ==2): #Subscribe to the topics
        do_subscribe(MQTT_CREDENTIALS,JSON)
    if else(act_code ==3): #Publish to a topic
        publish_answer = do_publish(MQTT_CREDENTIALS,JSON)
        
    else:
        print("WRONG ACTIVITY CODE")
        return -1
    return return_value;