# Configure recovery server and import images on NBU server.

Prepare NBU server.
-------------------
Prepare the NBU Primary Server, which will be configured as the CRS (Recovery Server). 
The NBU Primary Server used for CRS configuration must be version 11.0 or higher. 
Asset images created with NBU Primary version 10.5 or higher are supported for import into the configured CRS.

Prepare Automation Hosts/Ansible client.
-------------
1. Copy configure CRS code(the whole folder 'crs') to automation host.
2. Add NBU primay server to ansible config file.
3. For configure CRS, if KMS was enbaled, please get the kms file and kms variables.
4. If registering NBU primay server to Alta setup is needed, please add your server on Alta GUI and download registration file.

Update variables and encrypt it using ansible-vault if needed.
--------------------------------------------------------------
1. Update crs/roles/recovery-server/vars/main.yml
2. Run ansible-vault cmd to encrypt vars/main.yml and set password, This password will also be used to decrypt the vars/main.yml, please remember it.
   ```
   [root@vraqingv20041 vars]# ansible-vault encrypt main.yml
   New Vault password:
   Confirm New Vault password:
   Encryption successful

   ```

How to run ansible Playbooks
----------------------------
1. `playbook_configure_recovery_server_linux.yml` : Configure Netbackup as CRS server. 
    This playbook contains 3 part, for each part there is a flag,
    * configure_crs: yes
    * register_crs: yes
    * add_vcenter: no
    if set flag to 'yes', this step will be executed.
    if set flag to 'no', this step will be skipped.

    ```
    Running command example:
    ansible-playbook playbook_configure_recovery_server_linux.yml
    ```

2. `playbook_import_images_for_recovery_server_linux.yml` : Import images from Primary server to CRS server.
    Below parameters should be passed while running this playbook.
    * clientlist: []
    * policylist: []

    ```
    Running command example:
    ansible-playbook playbook_import_images_for_recovery_server.yml --extra-vars '{"clientlist":['test1.veritas.com', 'test2.veritas.com'],"policylist":['test-policy1', 'test-policy2']}'
    ```

How to execute playbook in blueprint job on AltaView GUI.
---------------------------------------------------------
There are 2 wrappers to run playbooks.
* `wrapper_configure_crs.py`: Execute playbook playbook_configure_recovery_server_linux.yml

* `wrapper_import_image.py` : Parse the clientlist and policylist parameter from AltaView GUI and execute playbook playbook_import_images_for_recovery_server_linux.yml


```
Once the automation hosts was registered and connected on AltaView, select above wrapper script to execute different task.
For import images, input parameter like below,

key               value
clientlist   test1.veritas.com,501c1693-9987-2c89-c0a8-e1edc29f392c
policylist   test-policy1,test-policy2
```

* Log file on automation hosts.
```
/var/log/cohesity/automation-host/automation-host.log
/var/log/cohesity/automation-host/crs_configure.log
/var/log/cohesity/automation-host/crs_import_image.log
```
* Log file on CRS server.
```
/var/log/puredisk/image_sharing_config.log
/var/log/crs/add_vcenter.log
/var/log/crs/import_images.log
/var/log/crs/register_to_alta.log
```
