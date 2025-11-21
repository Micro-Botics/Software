import machine
import network


def wifi_scan(json_entry_file):
    """
    json has a form of a list of dictionaries. Example:
    ({"ssid": ssid,
            "bssid/MAC": ":"11:11:11:11",
            "channel": channel,
            "rssi": rssi,
            "authmode": authmode,  # 0=open, 3=WPA2, etc.
            "hidden": BOOLEAN_VALUE}
            ,{...})

    Check whether the json_entry_file follows this logic and add all new APs that are not registered.

    """
    return json_entry_file
