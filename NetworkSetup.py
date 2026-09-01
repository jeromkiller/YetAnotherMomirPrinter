import subprocess
import socket
import json

data = None
with open("setup.json", "r") as file:
    data = json.load(file)

def getUnconnectedSSIDs(interface: str = "") -> list[str]:
    connected_ssid = getConnectedSSID()
    nearby_ssids = getNearbySSIDs(interface)

    if "momir_printer" in nearby_ssids:
        nearby_ssids.remove("momir_printer")
    if connected_ssid in nearby_ssids:
        nearby_ssids.remove(connected_ssid)
    return nearby_ssids

def getNearbySSIDs(interface: str = "") -> list[str]:
    discovery_command = ["/usr/bin/sudo", "/usr/bin/nmcli", "device", "wifi", "rescan"]
    discovery_read = ["/usr/bin/nmcli", "-t", "-f", "ssid", "device", "wifi", "list"]
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
    connected_ssid = subprocess.check_output(["/usr/sbin/iwgetid"]).decode('utf8').strip()
    if not connected_ssid:
        return "Unknown"
    connected_ssid = connected_ssid.split(":")[1].strip('"')
    return connected_ssid

def forgetNetwork(ssid: str):
    forget = ["/usr/bin/sudo", "/usr/bin/nmcli", "connection", "delete", ssid]
    if ssid:
        subprocess.run(forget)

def changeNetwork(ssid: str, password: str, hidden: bool):
    prev_connected_ssid = getConnectedSSID()
    connection = ["/usr/bin/sudo", "/usr/bin/nmcli", "dev", "wifi", "connect", ssid, "password", password, "hidden", "yes" if hidden else "no", "ifname", "wlan0"]
    try:
        output = subprocess.check_output(connection)
    except:
        # didn't succeed, try to remove the ssid
        forgetNetwork(ssid)

    new_connected_ssid = getConnectedSSID()
    if new_connected_ssid != prev_connected_ssid:
        forgetNetwork(prev_connected_ssid)

def testNetwork(host="8.8.8.8", port=53, timeout=3) -> bool:
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

def getLocalIp() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    s.close()
    return IPAddr

def getInternalIp() -> str:
    return "10.42.0.1"

def getWebPageUrl() -> str:
    return "http://" + getLocalIp()

def getSetupPageUrl() -> str:
    return "http://" + getInternalIp() + "/admin.html"

def getSetupSSID() -> str:
    return data.get("internal_ssid", "")

def getSetupPassword() -> str:
    return data.get("internal_pass", "")

def isSetupSSIDHidden() -> bool:
    return data.get("internal_hidden", "") == "true"
    