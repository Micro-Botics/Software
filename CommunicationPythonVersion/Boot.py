# boot.py -- run on boot-up
import network, utime, machine
"""
boot.py function to connect device to the wifi network, incase device is already connected it will test connection.
If test is passed it will return 1 , if test is failed it will try to reiniciate the connection, and test connection again, if subsequent test is failed
it will return 0.
"""

def do_connect_wifi(wifi_credentials):
    SSID = wifi_credentials["SSID"] #Name of a network connect to
    PASSWORD = wifi_credentials["PASSWORD"] #Password of a network. All this info is in a separate file
    sta_if = network.WLAN(network.STA_IF) #Creates interface to check connection and connect
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
    #print('Connected! Network config:', sta_if.ifconfig())
    connection_state = 1 if sta_if.isconnected() else 0
    return connection_state

do connect_mqtt


    