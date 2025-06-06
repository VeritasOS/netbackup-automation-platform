#!/usr/bin/python3
# $Copyright: Copyright (c) 2025 Veritas Technologies LLC. All rights reserved $

import os
import sys
import requests
import json
import urllib.parse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
from datetime import datetime, timedelta
import logging

# Suppress only the single InsecureRequestWarning from urllib3 needed
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


logger = None
def set_logger():
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    os.makedirs("/var/log/crs/", exist_ok=True)
    file_handler = logging.FileHandler('/var/log/crs/import_images.log')
    file_handler.setLevel(logging.DEBUG)
    log_formatter_file = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_formatter_file)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    log_formatter_console = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(log_formatter_console)
    logger.addHandler(console_handler)


def load_credentials(file_path):
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
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    
    if response.status_code == 201:
        logger.info("Login successful")
        return response.json()
    else:
        logger.error(f"Failed to login: {response.status_code}")
        logger.info(f"Login Response: {response.text}")
        return None

def get_disk_pools(server, token):
    url = f"https://{server}:443/netbackup/storage/disk-pools?sType eq 'PureDisk' and wormCapable eq true"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code == 200:
        logger.info("Disk pools retrieved successfully")
        return response.json()
    else:
        logger.error(f"Failed to retrieve disk pools: {response.status_code}")
        logger.info(f"Disk Pools Response:{response.text}")
        return None

def extract_disk_volume_names(disk_pools_response):
    volume_names = []
    for item in disk_pools_response['data']:
        for volume in item['attributes']['diskVolumes']:
            volume_names.append(volume['name'])
    return volume_names


def get_shared_images(server, token, lsu, filters):
    """
    filters sample:
    filters:{"start_time":30, "end_time":3, "clients":["clientA","clientB"], "policies":["policyA", "policyB"]}
    start_time: 30  # means 30 days ago.
    end_time: 3     # means 3 days ago.
    """
    start_time = ""
    end_time = ""
    client_list = []
    policy_list = []
    shared_images_list = []
    
    if "start_time" in filters:
        start_time = get_past_date(filters["start_time"])
    if "end_time" in filters:
        end_time = get_past_date(filters["end_time"])
    if "clients" in filters:
        client_list = filters["clients"]
    if "policies" in filters:
        policy_list = filters["policies"]

    if client_list:
        for client in client_list:
            images = Run_get_shared_images_api(server, token, start_time=start_time, end_time=end_time, client_name=client, lsu_name=lsu)
            if images:
                logger.info(f"Shared images retrieved successfully for client: {client}.\n")
                logger.info(f"Images: {images}")
                shared_images_list.append(images)
            else:
                logger.info(f"No images was retrived for client: {client}\n")
    if policy_list:
        for policy in policy_list:
            images = Run_get_shared_images_api(server, token, start_time=start_time, end_time=end_time, policy_name=policy, lsu_name=lsu)
            if images:
                logger.info(f"Shared images retrieved successfully for policy: {policy}.\n")
                logger.info(f"Images: {images}")
                shared_images_list.append(images)
            else:
                logger.info(f"No images was retrived for policy: {policy}.\n")

    if not policy_list and not client_list:
        images = Run_get_shared_images_api(server, token, start_time=start_time, end_time=end_time, lsu_name=lsu)
        if images:
            logger.info(f"Shared images retrieved successfully.\n")
            logger.info(f"Images: {images}")
            shared_images_list.append(images)
        else:
            logger.info(f"No images was retrived.\n")

    #logger.info(f"shared_images_list: {shared_images_list}")
    return shared_images_list

        
def Run_get_shared_images_api(server, token, start_time=None, end_time=None, client_name=None, policy_name=None, lsu_name=None):
    url = f"https://{server}/netbackup/storage/shared-images"
    filter_str = f"importStatus eq 'NotImported' and host eq '{server}'"
    if start_time:
        filter_str += f" and backupTime ge '{start_time}'"
    if end_time:
        filter_str += f" and backupTime le '{end_time}'"
    if client_name:
        filter_str += f" and client eq '{client_name}'"
    if policy_name:
        filter_str += f" and policy eq '{policy_name}'"
    if lsu_name:
        filter_str += f" and lsuName eq '{lsu_name}'"
        
    logger.info(f"Start to get images for filter\n:{filter_str}\n")
    
    params = {
        "page[limit]": 500,
        "page[offset]": 0,          
        "filter": filter_str
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "accept": "application/vnd.netbackup+json;version=12.0"
    }

    response = requests.get(url, headers=headers, params=params, verify=False)
    if response.status_code == 200:
        image = response.json()
        if image['data']:
            return image
        return None
    else:
        logger.error(f"Failed to retrieve shared images with return code: {response.status_code}")
        logger.info(f"Request URL: {response.url}")
        logger.info(f"Shared Images Response:{ response.text}\n")
        return None

def import_image(credentials, token, image, lsuname):
    url = f"https://{credentials['server']}/netbackup/catalog/cloud-images/import"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/vnd.netbackup+json;version=12.0",
        "accept": "application/vnd.netbackup+json;version=12.0"
    }
    payload = {
        "data": {
            "type": "importRequest",
            "attributes": {
                "host": credentials['server'],
                "lsuName": lsuname,
                "images": [image]
            }
        }
    }
    
    while True:
        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
        #logger.info(f"Import Request URL: {response.url}")
        #logger.info(f"Import Request Payload: {json.dumps(payload, indent=4)}")

        if response.status_code == 201:
            logger.info("Image import successful")
            return response.json()
        elif response.status_code == 406:
            error_response = response.json()
            if error_response.get('errorCode') == 4503:
                logger.info("Current active job count exceeds limitation. Retrying in 3 minute...")
                time.sleep(180)
                continue
        else:
            logger.error(f"Failed to import image: {response.status_code}")
            logger.info(f"Import Response: {response.text}")
            return None

def get_past_date(days):
    current_time = datetime.utcnow()
    past_time = current_time - timedelta(days=days) 
    formatted_time = past_time.strftime('%Y-%m-%dT%H:%M:%S.000Z') 
    return formatted_time


def main():
    if len(sys.argv) != 2:
        logger.error("Missing input parameters.")
        sys.exit(1)

    raw_paras = sys.argv[1]  
    paras = json.loads(raw_paras.replace("'", '"'))    
    #logger.debug(f"Parsed paras: {paras}")
    """
    paras sample:
    {"crs_server":"crs_server_hostname", "username":"user_name", "password":"***",
     "filters":{"start_time":30, "end_time":3, clients:["clientA","clientB"], policies:["policyA", "policyB"]}}
      #start_time: 30  # means 30 days ago.
      #end_time: 3     # means 3 days ago
    """
    credentials = {}
    crs_server = paras["crs_server"]
    credentials["server"]   = crs_server
    credentials["username"] = paras["username"]
    credentials["password"] = paras["password"]
    filters = paras["filters"]
    logger.info(f"Received filters: {filters} for crs server: {crs_server}")
    # Login to NetBackup
    login_response = login_to_netbackup(credentials)

    if not login_response:
        return 

    token = login_response["token"]

    disk_pools = get_disk_pools(credentials["server"], token)
    if disk_pools:
        volume_names = extract_disk_volume_names(disk_pools)
        if not volume_names:
            logger.info("No Volume is present, no need to import.")
            return 0

    for lsuname in volume_names: 
        shared_images_response = get_shared_images(credentials["server"], token, lsuname, filters)
        if not shared_images_response:
            logger.info(f"No shared images in {lsuname}, no need to import.")
            continue

        duplicate_image = []
        for item in shared_images_response:
            image_list =  item['data']
            if not image_list:
                continue
            for image in image_list:
                if image['attributes']['backupID'] in duplicate_image:
                    continue
                image_payload = {
                    "client": image['attributes']['client'],
                    "policy": image['attributes']['policy'],
                    "backupID": image['attributes']['backupID']
                    }  
                logger.info(f"Started image import for : {image['attributes']['backupID']}")
                import_image(credentials, token, image_payload, lsuname)
                duplicate_image.append(image['attributes']['backupID'])


if __name__ == "__main__":
    set_logger()
    logger.info(f"Running script: {__file__}")
    main()
