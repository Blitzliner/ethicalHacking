#!/usr/bin/env python3

import subprocess
import argparse
import re
import sys

def mac_changer(interface="eth0", new_mac="00:11:22:33:44:66"):
    print(F"Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])  # disable interface
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])  # enable interface
    print_list()


def print_list():
    ret = subprocess.check_output(["ifconfig", "-a"]).decode('ascii')
    find = r'^(\w+):.*?ether\s(.*?)\s'
    matches = re.findall(find, ret, flags=re.DOTALL)

    print("Aavailabe interfaces:")
    for m in matches:
        print(F"- {m[0]} {m[1]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", help="Change MAC address for this interface")
    parser.add_argument("-m", "--mac", help="New MAC address")
    parser.add_argument("-a", "--list_all", action="store_true",
                        help="List all available interfaces with their MAC address")

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.list_all:
        print_list()
    else:
        mac_changer(args.interface, args.mac)
