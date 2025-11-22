import network
import json
import time


def wifi_scan(json_entry_file):
    
    # Check whether the json file exists
    
    print("Checking gathered data...")
    try:
        with open(json_entry_file, "r") as f:
            json_data = json.load(f)
    except OSError:
            print("No valid JSON data found.")
            json_data = []

    # Check whether the json data is in the correct format

    if (check_json_format(json_data) == False):
        print("Invalid JSON format.")
        json_data = []
    else:
        print("Valid JSON format found.")

    # Scan for WiFi networks

    print("Scanning for WiFi networks...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    scan_results = wlan.scan()

    # Process scan results and add new entries to json_data

    for result in scan_results:
        ssid = result[0].decode() if isinstance(result[0], bytes) else result[0]
        bssid = ':'.join('{:02x}'.format(b) for b in result[1])  # convert MAC to readable string
        channel = result[2]
        rssi = result[3]
        auth_mode = result[4]
        hidden = result[5]

        new_entry = {
                "ssid": ssid,
                "bssid": bssid,
                "channel": channel,
                "rssi": rssi,
                "auth_mode": auth_mode,
                "hidden": hidden
        }

        if new_entry["bssid"] not in [entry["bssid"] for entry in json_data]:
            json_data.append(new_entry)

    return json_data

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)
    
def check_json_format(json_data):
    required_keys = {"ssid", "bssid", "channel", "rssi", "auth_mode", "hidden"}
    for entry in json_data:
        if not required_keys.issubset(entry.keys()):
            return False
    return True

################          ELIMINAR ESTO LUEGO              ################     

def main():
    wifi_scan_file = "wifi_scan.json"
    while True:
        networks = wifi_scan(wifi_scan_file)
        print("Found {} networks".format(len(networks)))

        save_json("wifi_scan.json", networks)
        print("Saved results to wifi_scan.json")
        print("Saved networks are: ",networks)

        time.sleep(10)  # Scan every 10 seconds (adjust as needed)


main()