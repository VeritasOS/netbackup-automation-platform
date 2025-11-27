#!/usr/bin/python3
# $Copyright: Copyright (c) 2025 Cohesity, Inc. All rights reserved $

import os
import sys
import csv
import subprocess
import traceback
import logging


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYBOOK_NAME = "playbook_import_images_for_recovery_server_linux.yml"
PLAYBOOK_PATH = os.path.join(CURRENT_DIR, PLAYBOOK_NAME)

LOG_PATH = "/var/log/cohesity/automation-host/crs_import_image.log"

logger = None
def set_logger():
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setLevel(logging.DEBUG)
    log_formatter_file = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_formatter_file)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    log_formatter_console = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(log_formatter_console)
    logger.addHandler(console_handler)


def run_cmd(command, cmdout=subprocess.PIPE, cmderr=subprocess.PIPE, quiet=False):
    """
    Run shell command and block the output untill the command completes
    """
    logger.info(f"Running command:\n{command}")
    subp = subprocess.Popen(command, shell=True, stdout=cmdout, stderr=cmderr, encoding="utf-8")
    out, err = subp.communicate()
    rc = subp.returncode

    if rc != 0 and err != '':
        logger.info(f"Error happened when run command: rc: {rc}\n{err}")
    else:
        logger.info(f"Run cmd successfully.\n{out}")

    return rc

# test,"client1,client2","policy1,policy2"
def parse_csv(csv_file):
    rows = []
    with open(csv_file, 'r' , encoding='utf-8') as csvfile:
        content = csv.reader(csvfile, delimiter=',')
        for row in content:
            rows.append(row)
    if len(rows) < 2:
        raise ValueError("CSV file must contain at least two lines.")
    keys = rows[0]
    values = rows[1]

    paras_dict = dict(zip(keys, values))
    return paras_dict

def run_ansible(paras):
    """
    1. Get paramters for policy_list and client_list.
       # "client1,client2","policy1,policy2"
    2. Run ansible playbook.
    """
    logger.info("Start to run ansible playbook.")
    policy_list = []
    client_list = []
    if "clientlist" in paras:
        client_list = paras["clientlist"].split(",")
    if "policylist" in paras:
        policy_list = paras["policylist"].split(",")
    logger.info(f"clientlist: {client_list}")
    logger.info(f"policy_list: {policy_list}")

    cmd = f"ansible-playbook {PLAYBOOK_PATH} --extra-vars " + "'{\"" + "clientlist" + "\":" +f"{client_list}" +",\""+ "policylist" + "\":" +f"{policy_list}" + "}'"
    rc = run_cmd(cmd)
    return rc

def main():
    logger.debug(f"Start to run script {__file__}")
    try:
        # set the ansible vault password environment.
        #os.environ['ANSIBLE_VAULT_PASSWORD'] = "test"
        if 'ANSIBLE_VAULT_PASSWORD' not in os.environ:
            logger.debug("the environment var ANSIBLE_VAULT_PASSWORD was not set.")
            return 1
        os.environ['ANSIBLE_VAULT_PASSWORD_FILE'] = os.path.join(CURRENT_DIR, "vault_pass")
    except Exception as err:
        traceback.print_exc()
        logger.error(f"Exception happened, {err}")
        return 1

    try:
        os.chdir(os.path.dirname(__file__))
        if len(sys.argv) < 2:
            logger.info("No input parameters were given from GUI, will try to import all images.")
            paras_dict = {}
        else:
            csv_file = sys.argv[1]
            logger.info(f"Input file received: {csv_file}")
            paras_dict = parse_csv(csv_file)

        return run_ansible(paras_dict)

    except Exception as err:
        traceback.print_exc()
        logger.info(f"Exception happened in main, {err}")
        return 1


if __name__ == '__main__':
    set_logger()
    main()
