import subprocess

def getUnconnectedSSIDs(interface: str = "") -> list[str]:
    connected_ssid = getConnectedSSID()
    nearby_ssids = getNearbySSIDs(interface)

    if "momir_printer" in nearby_ssids:
        nearby_ssids.remove("momir_printer")
    if connected_ssid in nearby_ssids:
        nearby_ssids.remove(connected_ssid)
    return nearby_ssids

def getNearbySSIDs(interface: str = "") -> list[str]:
    discovery_command = ["sudo", "nmcli", "device", "wifi", "rescan"]
    discovery_read = ["nmcli", "-t", "-f", "ssid", "device", "wifi", "list"]
    if interface:
        discovery_command += ["ifname", "wlan0"]
        discovery_read += ["ifname", "wlan0"]

    subprocess.run(discovery_command)
    nearby_ssids = subprocess.check_output(discovery_read).decode('utf8')
    ssid_set = set()
    for line in nearby_ssids.split("\n"):
        if not line:
            continue
        ssid_set.add(line)
    return list(ssid_set)

def getConnectedSSID() -> str:
    connected_ssid = subprocess.check_output(["iwgetid"]).decode('utf8').strip()
    if not connected_ssid:
        return "Unknown"
    connected_ssid = connected_ssid.split(":")[1].strip('"')
    return connected_ssid

def forgetNetwork(ssid: str):
    forget = ["sudo", "nmcli", "connection", "delete", ssid]
    if ssid:
        subprocess.run(forget)

def changeNetwork(ssid: str, password: str, hidden: bool):
    prev_connected_ssid = getConnectedSSID()
    connection = ["sudo", "nmcli", "dev", "wifi", "connect", ssid, "password", password, "hidden", "yes" if hidden else "no", "ifname", "wlan0"]
    try:
        output = subprocess.check_output(connection)
    except:
        # didn't succeed, try to remove the ssid
        forgetNetwork(ssid)

    new_connected_ssid = getConnectedSSID()
    if new_connected_ssid != prev_connected_ssid:
        forgetNetwork(prev_connected_ssid)
