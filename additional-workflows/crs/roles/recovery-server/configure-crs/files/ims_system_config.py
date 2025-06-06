#!/usr/openv/pdde/pdopensource/bin/python3
# $Copyright: Copyright (c) 2025 Veritas Technologies LLC. All rights reserved $

import sys
#ver = f"{sys.version_info.major}.{sys.version_info.minor}"
#sys.path.append(0, f'/usr/openv/pdde/pdshared/lib/python{ver}/site-packages')
from six.moves import range
from six.moves import input
import argparse
import logging
import os
import queue
import re
import requests
import shlex
import socket
import subprocess
import time
import traceback
import threading
import json
import signal
import atexit
from base64 import urlsafe_b64encode
from urllib3.exceptions import InsecureRequestWarning

json_file = "crs_api_payload_template.json"

logger = None
msdp_cloud_storage_type = 'PureDisk'
reserved_free_space_percent = 10
cloud_data_cache_size_min = 10
cloud_data_cache_size_max = 500
cloud_meta_cache_size_default = 10
cloud_map_cache_size_default = 5


aws_region_info = {
"us-east-2": "US East (Ohio)",
"us-east-1": "US East (N. Virginia)",
"us-west-1": "US West (N. California)",
"us-west-2": "US West (Oregon)",
"af-south-1": "Africa (Cape Town)",
"ap-east-1": "Asia Pacific (Hong Kong)",
"ap-south-2": "Asia Pacific (Hyderabad)",
"ap-southeast-3": "Asia Pacific (Jakarta)",
"ap-southeast-4": "Asia Pacific (Melbourne)",
"ap-south-1": "Asia Pacific (Mumbai)",
"ap-northeast-3": "Asia Pacific (Osaka)",
"ap-northeast-2": "Asia Pacific (Seoul)",
"ap-southeast-1": "Asia Pacific (Singapore)",
"ap-southeast-2": "Asia Pacific (Sydney)",
"ap-northeast-1": "Asia Pacific (Tokyo)",
"ca-central-1": "Canada (Central)",
"ca-west-1": "Canada West (Calgary)",
"cn-north-1": "China (Beijing)",
"cn-northwest-1": "China (Ningxia)",
"eu-central-1": "Europe (Frankfurt)",
"eu-west-1": "Europe (Ireland)",
"eu-west-2": "Europe (London)",
"eu-south-1": "Europe (Milan)",
"eu-west-3": "Europe (Paris)",
"eu-south-2": "Europe (Spain)",
"eu-north-1": "Europe (Stockholm)",
"eu-central-2": "Europe (Zurich)",
"il-central-1": "Israel (Tel Aviv)",
"me-south-1": "Middle East (Bahrain)",
"me-central-1": "Middle East (UAE)",
"sa-east-1": "South America (São Paulo)"
}


def cleanup():
    pass
atexit.register(cleanup)


help_str = {}
def get_full_help_str(help_str_key, seperator_char='/'):
    ret = ''
    if type(help_str[help_str_key]) is list:
        for index in range(len(help_str[help_str_key])):
            if index != 0:
                ret += seperator_char
            ret += help_str[help_str_key][index]
    else:
        ret = help_str[help_str_key]
    return ret


def valid_cache_size(cache_size, minimum = -1):
    try:
        cache_size = int(cache_size)
    except Exception:
        return False
    if minimum >= 0 and cache_size < minimum:
        return False
    return True

def get_cache_size_error_message(cache_type, cache_value, minimum_value = -1):
    error_message = 'Invalid input: {_cache_type} with value [{_cache_value}]. Only integer is acceptable.'\
        .format(_cache_type=cache_type, _cache_value=cache_value)
    if minimum_value >= 0:
        error_message += ' Minimum value is {_minimum_value}.'.format(_minimum_value=minimum_value)
    return error_message


def get_cache_size_ignore_message(cache_type, cache_value):
    return 'The {_cache_type} that you have specified [{_cache_value}] will be ignored since it is only applicable for PureDisk storage server.'\
        .format(_cache_type=cache_type, _cache_value=cache_value)


def get_disk_space_info(path):
    st = os.statvfs(path)
    total = st.f_blocks * st.f_frsize
    free = st.f_bavail * st.f_frsize
    return total, free


def log_disk_space(disk_total_bytes, disk_free_bytes, required_bytes, cloud_upload_cache_size_byte, cloud_map_cache_size_byte, cloud_meta_cache_size_byte, cloud_data_cache_size_byte, required_free_bytes, calc_free_bytes, automatic_calc):
    one_gib_bytes = 1024 * 1024 * 1024
    one_gib_bytes_float = float(one_gib_bytes)
    logger.info('Information about disk space required by MSDP Cloud of PureDisk storage server:')
    logger.info('Current total disk space of mount point [%s] is %.2f GiB.' , args.mount_point, disk_total_bytes / one_gib_bytes_float)
    logger.info('Current free disk space of mount point [%s] is %.2f GiB.' , args.mount_point, disk_free_bytes / one_gib_bytes_float)
    logger.info('Required disk space is %.2f GiB, including:', required_bytes / one_gib_bytes_float)
    logger.info('CLOUD_UPLOAD_CACHE_SIZE = %.2f GiB (fixed size)', cloud_upload_cache_size_byte / one_gib_bytes_float)
    logger.info('CLOUD_MAP_CACHE_SIZE = %.2f GiB', cloud_map_cache_size_byte / one_gib_bytes_float)
    logger.info('CLOUD_META_CACHE_SIZE = %.2f GiB', cloud_meta_cache_size_byte / one_gib_bytes_float)
    if automatic_calc:
        logger.info('CLOUD_DATA_CACHE_SIZE = %.2f GiB (automatically calculated)', cloud_data_cache_size_byte / one_gib_bytes_float)
    else:
        logger.info('CLOUD_DATA_CACHE_SIZE = %.2f GiB', cloud_data_cache_size_byte / one_gib_bytes_float)
    logger.info('Required reserving free space = %.2f GiB (Total disk space * %d%%)', required_free_bytes / one_gib_bytes_float, reserved_free_space_percent)
    logger.info('Left minimum free space = %.2f GiB', calc_free_bytes / one_gib_bytes_float)


def log_disk_full():
    logger.error('Disk free space is not enough. (Left minimum free space is less than required reserved free space)')

def check_disk_free_space():
    disk_total_bytes, disk_free_bytes = get_disk_space_info(args.mount_point)
    one_gib_bytes = 1024 * 1024 * 1024
    required_min_free_bytes = int(disk_total_bytes * reserved_free_space_percent / 100.0) + 1
    cloud_upload_cache_size_byte = one_gib_bytes
    cloud_map_cache_size_byte = int(args.cloud_map_cache_size) * one_gib_bytes
    cloud_meta_cache_size_byte = int(args.cloud_meta_cache_size) * one_gib_bytes
    if args.cloud_data_cache_size:
        cloud_data_cache_size_byte = int(args.cloud_data_cache_size) * one_gib_bytes
        required_bytes = cloud_upload_cache_size_byte + cloud_map_cache_size_byte + cloud_meta_cache_size_byte + cloud_data_cache_size_byte
        usable_free_bytes = disk_free_bytes - required_bytes
        log_disk_space(disk_total_bytes, disk_free_bytes, required_bytes, cloud_upload_cache_size_byte, cloud_map_cache_size_byte, cloud_meta_cache_size_byte, cloud_data_cache_size_byte, required_min_free_bytes, usable_free_bytes, False)
        if usable_free_bytes <= required_min_free_bytes:
            log_disk_full()
            return 1
    else:
        min_cloud_data_cache_size_byte = 10 * one_gib_bytes
        cloud_data_cache_size_byte = min_cloud_data_cache_size_byte
        required_bytes = cloud_upload_cache_size_byte + cloud_map_cache_size_byte + cloud_meta_cache_size_byte + min_cloud_data_cache_size_byte
        usable_free_bytes = disk_free_bytes - required_bytes
        if usable_free_bytes > required_min_free_bytes:
            cloud_data_cache_size_byte = disk_free_bytes - cloud_upload_cache_size_byte - cloud_map_cache_size_byte - cloud_meta_cache_size_byte - required_min_free_bytes
            cloud_data_cache_size = cloud_data_cache_size_byte // one_gib_bytes
            if cloud_data_cache_size > cloud_data_cache_size_max:
                cloud_data_cache_size = cloud_data_cache_size_max
            cloud_data_cache_size_byte = cloud_data_cache_size * one_gib_bytes
            required_bytes = cloud_upload_cache_size_byte + cloud_map_cache_size_byte + cloud_meta_cache_size_byte + cloud_data_cache_size_byte
            usable_free_bytes = disk_free_bytes - required_bytes
            log_disk_space(disk_total_bytes, disk_free_bytes, required_bytes, cloud_upload_cache_size_byte, cloud_map_cache_size_byte, cloud_meta_cache_size_byte, cloud_data_cache_size_byte, required_min_free_bytes, usable_free_bytes, True)
            args.cloud_data_cache_size = cloud_data_cache_size
        else:
            log_disk_space(disk_total_bytes, disk_free_bytes, required_bytes, cloud_upload_cache_size_byte, cloud_map_cache_size_byte, cloud_meta_cache_size_byte, cloud_data_cache_size_byte, required_min_free_bytes, usable_free_bytes, True)
            log_disk_full()
            return 1
    return 0


def check_input_args(args):
    if args.storage_type != msdp_cloud_storage_type:
        logger.error('Invalid storage_type %s. Only %s is supported.', args.storage_type, msdp_cloud_storage_type)
        return 1

    if ((args.master.strip() == '' and args.media.strip() != "" ) or (args.master.strip() != '' and args.media.strip() == "" )):
        logger.warning("Enter the master and media server at the same time.")
        return 1

    if args.cloud_provider == 'aws':
        if not args.region:
            args.region = 'us-east-1' # Defaut region is us-east-1
        if not args.cloud_instance:
            if args.region.startswith('cn-'):
                # Use amazon.cn for cn-* region
                args.cloud_instance = 'amazon.cn'
            else:
                args.cloud_instance = 'amazon.com'
        if not args.provider_type:
            args.provider_type = 'amazon'
    elif args.cloud_provider == 'azure':
        if not args.cloud_instance:
            args.cloud_instance = 'my-azure'
        if args.region:
            logger.warning('The region that you have specified [%s] will be ignored by Microsoft Azure.', args.region)
            args.region = ''
        if not args.provider_type:
            args.provider_type = 'azure'
    else:
        pass

    global kms_config_file

    if not (os.path.exists(args.mount_point)):
        os.makedirs(args.mount_point)
    elif (os.listdir(args.mount_point)):
        logger.error("mount_point: %s is not empty,please clean the folder!", args.mount_point)
        return 1

    if not valid_cache_size(args.cloud_map_cache_size):
        logger.error(get_cache_size_error_message('CLOUD_MAP_CACHE_SIZE', args.cloud_map_cache_size))
        return 1
    if not valid_cache_size(args.cloud_meta_cache_size):
        logger.error(get_cache_size_error_message('CLOUD_META_CACHE_SIZE', args.cloud_meta_cache_size))
        return 1
    if not valid_cache_size(args.cloud_data_cache_size, cloud_data_cache_size_min):
        logger.error(get_cache_size_error_message('CLOUD_DATA_CACHE_SIZE', args.cloud_data_cache_size, 10))
        return 1
        #ret = check_disk_free_space()
        #if 0 != ret:
        #    return ret
    #else:
        #ret = check_disk_free_space()
        #if 0 != ret:
        #    return ret

    return 0


def check_hostname(args):
    print(('''
*****************************IMPORTANT TIPS!*********************************
Ensure that the hostname "%s" is in the FQDN format.
If the hostname is not in the FQDN format, the webservice might fail.''' % args.storage_server))
    prompt = input("Enter Y to continue or any other key to reset:")
    if prompt == 'Y' or prompt == 'y':
        return 0
    else:
        return 1


def set_logger():
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('/var/log/puredisk/image_sharing_config.log')
    file_handler.setLevel(logging.DEBUG)
    log_formatter_file = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_formatter_file)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    log_formatter_console = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(log_formatter_console)
    logger.addHandler(console_handler)


def verify_msdp_webservice():
    cmd = ["/usr/openv/pdde/vpfs/bin/nb_admin_tasks", "--get_self_cert"]
    logger.info("[CMD]:%s", ' '.join(cmd))
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        logger.error("Ret:%d with message:%s", e.returncode, e.output)
        return 1

    return 0


def runCommand(command, cmdout=subprocess.PIPE, cmderr=subprocess.PIPE, quiet=False):
    """
    Run shell command and block to print/log the output untill the command completes
    """
    subp = subprocess.Popen(command, shell=True, stdout=cmdout, stderr=cmderr, encoding="utf-8")
    out, err = subp.communicate()
    rc = subp.returncode

    if rc != 0 and err != '':
        logger.error("error: is {} and rc {}".format(err, rc))
    else:
        logger.info("Run cmd successfully rc = {}".format(rc))

    return out, err, rc


def getNbuToken(master_server):
    nbapiutil_cmd = ['/usr/openv/pdde/pdcr/bin/nbapiutil', '--get_token', '--server', master_server]
    try:
        token = subprocess.check_output(nbapiutil_cmd, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        logger.error('%s failed with status %d. %s', ' '.join(nbapiutil_cmd), e.returncode, e.output)
        raise e
    return token.strip()


def getNbuTokenFromApi(primaryServer, userName, password):
    """
    This function is used for get nbu token.
    """
    apiUrl = "https://" + primaryServer + "/netbackup/login"
    headers = {}
    headers["content-type"] = "application/vnd.netbackup+json;version=12.0"
    reqbody = {}
    reqbody["userName"] = userName
    reqbody["password"] = password

    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.post(apiUrl, json=reqbody, headers=headers, verify=False)
    if response.status_code != 201:
        logger.error(f"Failied to get the netbackup token. details: {response}")
        return None

    logger.info("Get the netbackup token successfully.")
    return response.json()['token']


def runPostToNbuApi(apiUrl, reqbody, token, apicalltype='json'):
    """
    This function is used for sending post api request to nbu primary server.
    """
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    headers = {}
    headers["Authorization"] = 'Bearer ' + token
    headers["content-type"] = "application/vnd.netbackup+json;version=12.0"

    if apicalltype == "file":
        response = requests.post(apiUrl, files=reqbody, headers=headers, verify=False)
    else:
        response = requests.post(apiUrl, json=reqbody, headers=headers, verify=False)

    statusCode = response.status_code
    if statusCode == 201 or statusCode == 200:
        return True, response.json()
    if statusCode == 204:
        #when return code is 204, response is: <Response [204]>
        return True, response

    logger.info(f"runPostToNbuApi return code is: {statusCode}.\nResponse body is {response.json()}")
    return False, response.json()


def runGetToNbuApi(apiUrl, token, params):
    """
    This function is used for sending get api request to nbu primary server.
    """
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    headers = {}
    headers["Authorization"] = 'Bearer ' + token
    headers["content-type"] = "application/vnd.netbackup+json;version=12.0"
    response = requests.get(url=apiUrl, headers=headers, verify=False, params=params)

    statusCode = response.status_code
    if statusCode == 200:
        return True, response.json()
    else:
        logger.info(f"runGetToNbuApi return code is: {statusCode}.\nResponse body is {response.json()}")
        return False, response.json()


def createStorageServer(args, payload):
    primaryServer = args.master
    sts_usernm = urlsafe_b64encode(args.key_id.encode('utf-8')).decode('utf-8')[:8]
    sts_passwd = urlsafe_b64encode(args.secret_key.encode('utf-8')).decode('utf-8')[:12]
    token = getNbuToken(primaryServer)
    if not token:
        logger.error("Failed to get token.")
        return 1

    logger.info("Get NBU token successfully.")

    createStoragePathCmd = 'sudo mkdir ' + args.mount_point + '; sudo chmod -R 777 ' + args.mount_point
    out, err, rc = runCommand(createStoragePathCmd)
    if rc == 0:
        logger.info("Create storage path successfully.")
    else:
        logger.error("Failed to Create storage path.")
        return rc

    logger.info("Start to create storage server.")
    apiUrl = 'https://' + primaryServer + '/netbackup/storage/storage-servers'
    reqbody = payload["createStorageServer"]
    reqbody['data']['attributes']['name'] = args.storage_server
    reqbody['data']['attributes']['mediaServerDetails']['name'] = args.media
    reqbody['data']['attributes']['msdpAttributes']['storagePath'] = args.mount_point
    reqbody['data']['attributes']['msdpAttributes']['credentials']['userName'] = sts_usernm
    reqbody['data']['attributes']['msdpAttributes']['credentials']['password'] = sts_passwd
    reqbody['data']['attributes']['msdpAttributes']['imageSharingInCloud'] = True
    if args.kms_enabled == '1':
        reqbody['data']['attributes']['encryptionEnabled'] = True
        reqbody['data']['attributes']['kmsEnabled'] = True
        reqbody['data']['attributes']['kmsKeyGroupName'] = args.kms_key_group
    else:
        reqbody['data']['attributes']['encryptionEnabled'] = False

    rc, resJson = runPostToNbuApi(apiUrl, reqbody, token)
    if not rc:
        logger.error(f"Failed to create storage server.\nDetails: {resJson}")
        return 1

    logger.info("Create storage server successfully.")
    return 0


def createCredential(args, payload):
    primaryServer = args.master
    token = getNbuToken(primaryServer)
    if not token:
        logger.error("Failed to get NBU token.")
        return False

    logger.info("Get NBU token successfully.")

    # create credential
    logger.info("Start to create credential.")
    apiUrl = 'https://' + primaryServer + '/netbackup/config/credentials?meta=accessControlId'
    reqbody = payload["createCrendential"]
    # aws/azure rvlt
    if 'refresh_token' in reqbody['data']['attributes']['contents']:
        reqbody['data']['attributes']['contents']['refresh_token'] = args.secret_key
    # Only azure rvlt need this value.
    if 'storage_account' in reqbody['data']['attributes']['contents']:
        reqbody['data']['attributes']['contents']['storage_account'] = args.key_id
    # aws msdp_c
    if 'access_key_id' in reqbody['data']['attributes']['contents']:
        reqbody['data']['attributes']['contents']['access_key_id'] = args.key_id
        reqbody['data']['attributes']['contents']['secret_access_key'] = args.secret_key
    # azure msdp_c
    if 'access_key' in reqbody['data']['attributes']['contents']:
        reqbody['data']['attributes']['contents']['storage_account'] = args.key_id
        reqbody['data']['attributes']['contents']['access_key'] = args.secret_key

    rc, resJson = runPostToNbuApi(apiUrl, reqbody, token)
    if not rc:
        logger.error(f"Failed to create credential.\nDetails: {resJson}")
        return False

    logger.info("Create credential successfully.")
    return True


def createDiskVolume(args, payload):
    primaryServer = args.master
    token = getNbuToken(primaryServer)
    if not token:
        logger.error("Failed to get NBU token.")
        return 1
    logger.info("Get NBU token successfully.")
    if args.key_id != 'dummy':
        if not createCredential(args, payload):
            return 1
    logger.info("Get credential successfully.")

    logger.info("Start to create disk volume.")
    # need check we should use storage_server or media_server here?
    apiUrl = 'https://' + primaryServer + '/netbackup/storage/storage-servers/PureDisk:' + args.storage_server + '/disk-volumes'
    if args.crs_type == 'msdp-c' and args.key_id == 'dummy' and args.secret_key == 'dummy':
        reqbody = payload['createDiskVolumeWithRole']
    else:
        reqbody = payload['createDiskVolume']

    reqbody['data']['attributes']['diskVolumeName'] = args.bucket_sub_name
    reqbody['data']['attributes']['requestCloudCacheCapacity'] = args.cloud_data_cache_size
    reqbody['data']['attributes']['cloudAttributes']['bucketName'] = args.bucket_name
    reqbody['data']['attributes']['cloudAttributes']['subBucketName'] = args.bucket_sub_name
    if args.kms_enabled == '1':
        reqbody['data']['attributes']['encryptionEnabled'] = True
        reqbody['data']['attributes']['kmsEnabled'] = True
    else:
        reqbody['data']['attributes']['encryptionEnabled'] = False
        reqbody['data']['attributes']['kmsEnabled'] = False
    # aws
    if args.cloud_provider == 0:
        reqbody['data']['attributes']['region'] = args.region
        reqbody['data']['attributes']['cloudAttributes']['s3RegionDetails'][0]['regionId'] = args.region
        reqbody['data']['attributes']['cloudAttributes']['s3RegionDetails'][0]['regionName'] = aws_region_info[args.region]
        if not args.s3_host:
            args.s3_host = "s3.dualstack.{}.amazonaws.com".format(args.region)
        reqbody['data']['attributes']['cloudAttributes']['s3RegionDetails'][0]['serviceHost'] = args.s3_host
        reqbody['data']['attributes']['cloudAttributes']['serviceEndpoint'] =  args.s3_host

    rc, resJson = runPostToNbuApi(apiUrl, reqbody, token)
    if not rc:
        logger.error(f"Failed to create disk volume.\nDetails: {resJson}")
        return 1

    logger.info("Create disk volume successfully.")
    return 0


def createDiskPool(args, payload):
    primaryServer = args.master
    token = getNbuToken(primaryServer)
    if not token:
        logger.error("Failed to get NBU token.")
        return 1
    logger.info("Get NBU token successfully.")

    logger.info("Start to create disk pool.")
    apiUrl = 'https://' + primaryServer + '/netbackup/storage/disk-pools'
    reqbody = payload['createDiskPool']
    reqbody['data']['attributes']['diskVolumes'][0]['name'] = args.bucket_sub_name
    reqbody['data']['relationships']['storageServers']['data'][0]['id'] = 'PureDisk:' + args.storage_server

    rc, resJson = runPostToNbuApi(apiUrl, reqbody, token)
    if not rc:
        logger.error(f"Failed to create disk pool.\nDetails: {resJson}")
        return 1

    logger.info("Create disk pool successfully.")
    return 0


def importKmsKey(args):
    logger.info("Start to import kms key ...")
    token = getNbuToken(args.master)
    if not token:
        logger.error("Failed to get token.")
        return 1
    logger.info("Get NBU token successfully.")

    apiUrl = 'https://' + args.master + "/netbackup/security/key-management-services/nbkms/import"

    reqbody = {}
    reqbody['data'] = {}
    reqbody['data']['type'] = 'keyImportConfiguration'
    reqbody['data']['attributes'] = {}
    reqbody['data']['attributes']['passphrase'] = args.kms_passphrase
    reqbody['data']['attributes']['preserveKgName'] = True
    reqbody['data']['attributes']['comment'] = 'import kms key for image sharing'
    payload = {'kmsReqBody': json.dumps(reqbody)}
    files=[ ('importKeyFile', ('kms_kg_file',open(args.kms_file_name,'rb'), 'text/plain'))]

    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    headers = {}
    headers['Authorization'] = "Bearer " + token
    #headers['Content-Type'] = "multipart/vnd.netbackup+form-data;"

    response = requests.post(apiUrl, headers=headers, data=payload, files=files, verify=False)
    statusCode = response.status_code
    logger.info(f"response for import kms key:\nreturn code:{statusCode}\n{response.text}")
    if statusCode == 201 or statusCode == 200:
        logger.info("Import key successfully.")
        return 0
    elif re.search("a duplicate of existing key", response.text):
        return 0
    else:
        logger.error(f"Failed to import key.")
        return 1


def createNbKms(args):
    logger.info("Start to create nbkms ...")
    passphrase = args.kms_passphrase
    createNbkmsCmd = 'echo -e "{0}\n{0}\n1\n1\n1\n1\n" | /usr/openv/netbackup/bin/nbkms -createemptydb'.format(passphrase)
    out, err, rc = runCommand(createNbkmsCmd)
    if rc == 0:
        logger.info("Create nbkms successfully.")
    else:
        kmsServiceRunning = 'An instance of the KMS service is running'
        if kmsServiceRunning in err:
            logger.info("Create nbkms successfully.")
        else:
            logger.error("Failed to create nbkms.")
            return rc

    # discover nbkms
    discoverNbkmsCmd = '/usr/openv/netbackup/bin/nbkmscmd -discovernbkms -autodiscover'
    out, err, rc = runCommand(discoverNbkmsCmd)
    if rc == 0:
        logger.info("Discover nbkms successfully.")
    else:
        logger.error("Failed to discover nbkms.")
    return rc


def signal_handler(signal, frame):
    sys.exit(1)

def installSoftware():
    logger.info("Start to install software ...")
    createAzRepo = 'echo -e "[azure-cli]\n\
name=Azure CLI\n\
baseurl=https://packages.microsoft.com/yumrepos/azure-cli\n\
enabled=1\n\
gpgcheck=1\n\
gpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/azure-cli.repo'
    out, err, rc = runCommand(createAzRepo)
    if rc == 0:
        logger.info("Install azure cli repo successfully.")
    else:
        logger.error("Failed to install azure cli repo.")
    installSshPass = 'echo -e "y" | sudo yum install azure-cli'
    out, err, rc = runCommand(installSshPass)
    if rc == 0:
        logger.info("Install azure cli successfully.")
    else:
        logger.error("Failed to install azure cli.")
    return rc

def downloadKmsKey(args):
    downloadCmd = 'az storage blob download --account-name ' + args.kms_storage_account + ' --container-name ' + args.kms_container_name \
        + ' --name ' + args.kms_file_name + ' --file ' + args.kms_file_name + ' --auth-mode key --account-key ' + args.kms_container_key
    out, err, rc = runCommand(downloadCmd)
    if rc == 0:
        logger.info("Install sshpass successfully.")
    else:
        logger.error("Failed to install sshpass.")
    return rc

def import_kms_key(args):
    """
    # 0. install azure-cli
    rc = installSoftware()
    if rc != 0:
        return rc
    # 1. download kms key
    rc = downloadKmsKey(args)
    if rc != 0:
        return rc
    """
    # 2. create nbkms
    rc = createNbKms(args)
    if rc != 0:
        return rc

    # 3. import kms key
    rc = importKmsKey(args)
    if rc != 0:
        return rc
    return 0


def configure_storage_server(args, crs_payload):
    # create storage server
    rc  = createStorageServer(args, crs_payload)
    if rc != 0:
        return rc

    # create disk volume
    rc = createDiskVolume(args, crs_payload)
    if rc != 0:
        return rc

    # create disk pool
    rc = createDiskPool(args, crs_payload)
    if rc != 0:
        return rc

    return 0

def check_nbu_service(args):
    logger.info("Checking if NBU service is active...")
    try:
        token = getNbuToken(args.master)
        if not token:
            return False
        logger.info("NBU service check passed.")
        return True
    except Exception as err:
        logger.error(f"Exception happened in check_nbu_service, {err}\n")
        return False


def configure_crs(args):
    ret = check_input_args(args)
    if ret != 0:
        return 1

    logger.info(f"Ensure that the hostname {args.storage_server} is in the FQDN format.\nIf the hostname is not in the FQDN format, the webservice might fail.")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    #json_path = os.path.join(script_dir, json_file)
    json_path = "/tmp/.crs_api_payload_template.json"
    logger.info(f"Json template file path is {json_path}")
    with open(json_path, 'r') as fi:
        body = json.load(fi)
        crs_payload = body[args.cloud_provider][args.crs_type]

    if not args.master:
        args.master = args.storage_server
    if not args.media:
        args.media = args.storage_server

    if not check_nbu_service(args):
        return 1

    if args.kms_enabled == '1':
        logger.info("kms enabled, importing kms key...")
        ret = import_kms_key(args)
        if ret != 0:
            logger.info("Failed to import kms key")
            return 1
        logger.info("Import kms key successfully")

    logger.info("Begin configuring storage server...")
    ret = configure_storage_server(args, crs_payload)
    if ret != 0:
        logger.info("Aborted configuring storage server.")
        return 1
    logger.info("Completed configuring storage server.")
    return 0


def main(args):
    # Handle ctrl+c
    signal.signal(signal.SIGINT, signal_handler)
    set_logger()
    try:
        logger.info("Begin configuring crs...")
        ret = configure_crs(args)
        if ret != 0:
            logger.info("Failed configuring crs.")
            return 1
        logger.info("Completed crs configure.")

        time.sleep(10)
        logger.info("Begin verifying web service...")
        ret = verify_msdp_webservice()
        if ret != 0:
            logger.info("Aborted verifying web service.")
            return 1

        logger.info("Completed verifying web service.")
        return 0
    except Exception as err:
        traceback.print_exc()
        msg = f"Exception happened:\n{err}"
        logger.error(msg)
        return 1


def get_options():
    parser = argparse.ArgumentParser(description="CRS configuration")
    parser.add_argument("-o", "--option", type=str, choices=['crs', 'scanhost'], default='crs', help="the option which will be configured.")
    parser.add_argument("-cp", "--cloud_provider", type=str, default='aws', choices=['azure', 'aws'], help="The cloud provider.")
    parser.add_argument('-ct', '--crs_type', required=False, default='msdp-c',choices=['msdp-c', 'rvlt'], help="CRS type, msdp-c or rvlt")
    parser.add_argument('-k', '--key_id', required=True, default='', help='Amazon Web Services access key ID; Microsoft Azure storage account name; Third-party S3 access key ID')
    parser.add_argument('-s', '--secret_key', required=True, default='', help='Amazon Web Services secret access key; Microsoft Azure storage access key; Third-party S3 secret access key')
    parser.add_argument('-b', '--bucket_name', required=True, default='', help='Amazon Web Services S3 bucket name; Microsoft Azure storage container name;Third-party S3 bucket name')
    parser.add_argument('-bs', '--bucket_sub_name', required=True, default='', help='Amazon Web Services S3 bucket sub name; Microsoft Azure storage container sub name; Third-party S3 bucket sub name')
    parser.add_argument('-m', '--storage_server', required=False, default=socket.gethostname(),  help='storage server name')
    parser.add_argument('-t', '--storage_type', required=False, default='PureDisk',  help='storage server type (default is PureDisk)')
    parser.add_argument('-p', '--mount_point', required=False, default='/storage',  help='storage path (default is "/storage")')
    parser.add_argument('-c', '--cloud_instance', required=False, default='', help='cloud instance name of NetBackup')
    parser.add_argument('-e', '--kms_enabled', required=False, default='0', help='enabled/disabled kms encryption (default is 0)')
    parser.add_argument('-ka', '--kms_storage_account', required=False, help='kms storage account')
    parser.add_argument('-kn', '--kms_container_name', required=False, help='kms container name')
    parser.add_argument('-kf', '--kms_file_name', required=False, help='kms key file name')
    parser.add_argument('-kk', '--kms_container_key', required=False, help='kms container key')
    parser.add_argument('-kg', '--kms_key_group', required=False, help='kms key group')
    parser.add_argument('-kp', '--kms_passphrase', required=False, help='kms passphrase')
    parser.add_argument('-r', '--region', required=False, default='', help='Amazon Web Services service region (default is us-east-1)')
    parser.add_argument('-ms', '--master', required=False, default='', help='Master server that the bucket belongs to')
    parser.add_argument('-pu', '--primary_user_name', required=False, default='', help='User name of primary server')
    parser.add_argument('-pp', '--primary_password', required=False, default='', help='Password of primary server user')
    parser.add_argument('-ma', '--media', required=False, default='', help='Media server that the bucket belongs to')
    parser.add_argument('-sn', '--sts_number', required=False, default='', help='Number of Storage Server, only used for media server case')
    parser.add_argument('-pt', '--provider_type', required=False, default='', help='Third-party S3 cloud provider type')
    parser.add_argument('-sh', '--s3_host', required=False, default='', help='Third-party S3 server host name')
    parser.add_argument('-sp', '--s3_http_port', required=False, type=int, default=80, help='Third-party S3 server http port (default is 80)')
    parser.add_argument('-sps', '--s3_https_port', required=False, type=int, default=443, help='Third-party S3 server https port (default is 443)')
    parser.add_argument('-ssl', '--ssl', required=False, default='1', help='Third-party S3 server SSL usage: 0: Disable SSL. 1: Enable SSL. (default is 1)')
    parser.add_argument('-csd', '--cloud_data_cache_size', required=False, default=cloud_data_cache_size_min, help='Cloud data cache size of PureDisk storage server (integers in GiB, default is all available free disk space excluding {0}%% of total disk space.)'.format(reserved_free_space_percent))
    parser.add_argument('-csm', '--cloud_meta_cache_size', required=False, default=cloud_meta_cache_size_default, help='Cloud metadata cache size of PureDisk storage server (integers in GiB)')
    parser.add_argument('-csma', '--cloud_map_cache_size', required=False, default=cloud_map_cache_size_default, help='Cloud map cache size of PureDisk storage server (integers in GiB)')
    my_args = parser.parse_args()
    return my_args


if __name__ == "__main__":
    args = get_options()
    rc = main(args)
    sys.exit(rc)

