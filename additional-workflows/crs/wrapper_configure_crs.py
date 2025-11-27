#!/usr/bin/python3
# $Copyright: Copyright (c) 2025 Cohesity, Inc. All rights reserved $

import os
import sys
import subprocess
import traceback
import logging

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYBOOK_NAME = "playbook_configure_recovery_server_linux.yml"
PLAYBOOK_PATH = os.path.join(CURRENT_DIR, PLAYBOOK_NAME)
LOG_PATH = "/var/log/cohesity/automation-host/crs_configure.log"

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
        logger.error(f"Error happened when run command: rc: {rc}\n{err}")
    else:
        logger.info(f"Run cmd successfully.\n{out}")

    return rc


def parse_csv(csv_file):
    with open(csv_file, 'r' , encoding='utf-8') as csvfile:
        lines = csvfile.readlines()
    if len(lines) < 2:
        raise ValueError("CSV file must contain at least two lines.")
    key = lines[0].strip()
    value = lines[1].strip()
    logger.info(f"Received the key: {key} from GUI.")
    return {key: value}

def run_ansible():
    """
    1. Run ansible playbook.
    """
    logger.info("Start to run ansible playbook.")
    cmd = f"ansible-playbook {PLAYBOOK_PATH}"
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
        return run_ansible()

    except Exception as err:
        traceback.print_exc()
        logger.error(f"Exception happened in main, {err}")
        return 1

if __name__ == '__main__':
    set_logger()
    main()
