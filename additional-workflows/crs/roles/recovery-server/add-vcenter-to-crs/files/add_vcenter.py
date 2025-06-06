#!/usr/bin/python3
# $Copyright: Copyright (c) 2025 Veritas Technologies LLC. All rights reserved $

import os
import sys
import json
import requests
import urllib.parse
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = None

def set_logger():
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    os.makedirs("/var/log/crs/", exist_ok=True)
    file_handler = logging.FileHandler('/var/log/crs/add_vcenter.log')
    file_handler.setLevel(logging.DEBUG)
    log_formatter_file = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_formatter_file)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    log_formatter_console = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(log_formatter_console)
    logger.addHandler(console_handler)


def login_to_netbackup(credentials):
    url = f"https://{credentials['server']}:443/netbackup/login"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "userName": credentials['username'],
        "password": credentials['password']
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    
    if response.status_code == 201:
        logger.info("Login successful")
        return response.json()
    else:
        logger.error(f"Failed to login: {response.status_code}")
        logger.info(f"Login Response: {response.text}")
        return None

def add_vc(credentials, token, payload):
    url = f"https://{credentials['server']}:443/netbackup/config/servers/vmservers"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "accept": "application/vnd.netbackup+json;version=12.0"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    logger.info(f"Add vcenter response: {response.text}")

    if response.status_code == 201:
        logger.info("Added VCenter details successfully")
        return
    if response.status_code == 409:
        logger.info("VCenter has already been added.")
        return
    else:
        logger.error(f"Failed to add VCenter with status code {response.status_code}")
        return

def main():
    if len(sys.argv) != 2:
        logger.error("Missing input parameters.")
        sys.exit(1)
   
    raw_paras = sys.argv[1]
    paras = json.loads(raw_paras.replace("'", '"'))
    #logger.debug(f"Parsed paras: {paras}")

    credentials = {}
    credentials["server"]   = paras["crs_server"]
    credentials["username"] = paras["username"]
    credentials["password"] = paras["password"]

    payload = {"vmType": "VMWARE_VIRTUAL_CENTER_SERVER", "port": 0, "validate": True}
    payload["proxy"] = paras["crs_server"]
    payload["serverName"] = paras["vcenter_server_name"]
    payload["userId"] = paras["vcenter_user"]
    payload["password"] = paras["vcenter_password"]
    if "vmType" in paras:
        payload["vmType"] = paras["vmType"]
    if "port" in paras:
        payload["port"] = paras["port"]
    if "validate" in paras:
        payload["validate"] = paras["validate"]

    # Login to NetBackup
    login_response = login_to_netbackup(credentials)
    
    if login_response:
        token = login_response["token"]
        add_vc(credentials, token, payload)

if __name__ == "__main__":
    set_logger()
    logger.info(f"Running script: {__file__}")
    main()
