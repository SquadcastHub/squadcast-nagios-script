#!/usr/bin/env python3
#
# Python3 script to post Nagios alerts to Squadcast.
# This script has been tested with Python 3.7.4
#
import sys
import os
import json
import urllib.request

def print_usage():
    """Print the script usage"""
    print("Usage:\n  sq-nagios-service.py <url> <hostname> <service_description> <service_state> <service_output> <hostaddress>")

def form_payload(hostname = "", service_description = "",service_state = "",hostaddress = "",service_output = ""):
    """Forms the python representation of the data payload to be sent from the passed configuration"""

    payload_rep = {"hostname" : hostname,"servicedesc":service_description,"service_state":service_state,"hostaddress":hostaddress,"service_output":service_output,"alert_source":"SERVICE" }

    return payload_rep

def post_to_url(url, payload):
    """Posts the formed payload as json to the passed url"""
    try:
        headers={
        'User-Agent': 'squadcast',
        "Content-Type": "application/json"
        }
        req = urllib.request.Request(url, data=bytes(json.dumps(payload),"utf-8"),headers=headers)
        resp = urllib.request.urlopen(req)
        if resp.status > 299:
           print("[sq-nagios-service] Request failed with status code %s : %s" % (resp.status, resp.read()))
    except urllib.request.URLError as e:
        if e.code >= 400 and e.code < 500:
           print("[sq-nagios-service] Some error occured while processing the event")

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print_usage()
        exit(2)
    url =sys.argv[1]
    hostname = sys.argv[2]
    service_description = sys.argv[3]
    service_state = sys.argv[4]
    service_output = sys.argv[5]
    hostaddress = sys.argv[6]
    print("Sending data to squadcast")
    post_to_url(url, form_payload(hostname, service_description,service_state,hostaddress,service_output))
    print("Done.")
