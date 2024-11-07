#!/usr/bin/env python
import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change")
    parser.add_option("-m", "--mac", dest="mac", help="Mac_address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("Please input interface, use --help for more info.")
    elif not options.mac:
        parser.error("Please input mac_address, use --help for more info.")
    return options
def mac_changer_fun(interface,mac):
    subprocess.call(["sudo","ifconfig", interface, "down"])
    subprocess.call(["sudo","ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["sudo","ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_add_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_add_search:
        return mac_add_search.group(0)
    else:
        print("[-] Could not read mac address.")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC:", str(current_mac))
mac_changer_fun(options.interface, options.mac)
current_mac = get_current_mac(options.interface)

if str(current_mac) == options.mac:
    print("[+] Mac address was successfully changed to", current_mac)
else:
    print("[-] Mac address did not changed.")
