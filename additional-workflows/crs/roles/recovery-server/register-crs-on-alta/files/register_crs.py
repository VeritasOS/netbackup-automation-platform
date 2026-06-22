#!/usr/bin/python3
# $Copyright: Copyright (c) 2026 Cohesity, Inc. All rights reserved $

import os
import requests
import json
import sys
import logging
from urllib.parse import urlparse
import socket

# Certificate verification configuration
# Can be set via environment variable: NBU_CA_BUNDLE=/path/to/ca-bundle.crt
# If not set, defaults to True (uses system certificate store)
CA_BUNDLE = os.environ.get('NBU_CA_BUNDLE', True)
if CA_BUNDLE == 'False' or CA_BUNDLE == 'false':
    CA_BUNDLE = False

def get_verify_for_url(url):
    parsed = urlparse(url)
    local_names = {"localhost", "127.0.0.1", socket.gethostname()}
    if parsed.hostname in local_names:
        return False
    return CA_BUNDLE

logger = None

def set_logger():
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    os.makedirs("/var/log/crs/", exist_ok=True)
    file_handler = logging.FileHandler('/var/log/crs/register_to_alta.log')
    file_handler.setLevel(logging.DEBUG)
    log_formatter_file = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_formatter_file)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    log_formatter_console = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(log_formatter_console)
    logger.addHandler(console_handler)


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def login_to_netbackup(credentials):
    url = f"https://{credentials['server']}:443/netbackup/login"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "userName": credentials['username'],
        "password": credentials['password']
    }
    verify = get_verify_for_url(url)
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=verify)

    if response.status_code == 201:
        logger.info("Login successful")
        return response.json()
    else:
        logger.error(f"Failed to login: {response.status_code}")
        logger.info(f"Login Response: {response.text}")
        return None

def upload_json(credentials, token, file_path):
    url = f"https://{credentials['server']}/netbackup/alta-view/servers"
    headers = {
        "accept": "application/vnd.netbackup+json;version=12.0",
        "Authorization": f"Bearer {token}"
    }
    # Sending the JSON file as multipart/form-data with proxyEnabled as false
    files = {
        'file': ('registration.json', open(file_path, 'rb'), 'application/json'),
        "proxyEnabled": (None, "false"),
        "proxyId": (None, "")
    }

    verify = get_verify_for_url(url)
    response = requests.post(url, headers=headers, files=files, verify=verify)
    logger.info(f"Register api response: {response.text}")

    if response.status_code == 201:
        logger.info("Register server successfully.")
        return
    if response.status_code == 409:
        logger.info("The CRS server has already been registered.")
        return
    else:
        logger.error(f"API call failed with status code {response.status_code}")
        return

def main():
    if len(sys.argv) != 2:
        logger.error("Missing input parameters.")
        sys.exit(1)

    raw_paras = sys.argv[1]
    paras = json.loads(raw_paras.replace("'", '"'))

    credentials = {}
    credentials["server"]   = paras["crs_server"]
    credentials["username"] = paras["username"]
    credentials["password"] = paras["password"]

    registry_file = paras["alta_registry_file"]

    # Login to NetBackup
    login_response = login_to_netbackup(credentials)

    if login_response:
        token = login_response["token"]
        upload_json(credentials, token, registry_file)

if __name__ == "__main__":
    set_logger()
    logger.info(f"Running script: {__file__}")
    main()
