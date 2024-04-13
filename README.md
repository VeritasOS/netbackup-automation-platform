# NetBackup Automation Platform (NBAP)

## Description

Veritas NetBackup is the most powerful and widely adopted data protection solution in the world. NetBackup streamlines data protection management, protects your enterprise from the unforeseen, ensures business-critical resilience and delivers customer choice with a single platform supporting any workload, cloud and architecture at any scale.
The project contains Ansible roles and playbooks for automating the deployment and configuration of NetBackup. The roles and the playbooks are provided in order to demonstrate the automated NetBackup tasks and leverage NetBackup APIs in an automation workflow.<br>

> <span style="color:#0000ff"><b>NOTE:- </b></span> These playbooks support below NetBackup Client versions.<br>
> * <span style="color:#cc9900"><b>10.4.0.0</b></span><br>
> * <span style="color:#cc9900"><b>10.3.0.1</b></span><br>
> * <span style="color:#cc9900"><b>10.3.0.0</b></span><br>
> * <span style="color:#cc9900"><b>10.2.0.1</b></span><br>
> * <span style="color:#cc9900"><b>10.1.1.0</b></span><br>
> * <span style="color:#cc9900"><b>10.1.0.0</b></span><br>
> * <span style="color:#cc9900"><b>10.0.0.1</b></span><br>
> * <span style="color:#cc9900"><b>10.0.0.0</b></span><br>

## Project Contents

This project contains Ansible playbooks, roles, vars for automating various deployment tasks for NetBackup RHEL Client:

## Playbooks
##### All the playbooks are designed keeping the salient features of ansible into consideration.
- <span style="color:green"><b>Idempotent</b> in nature</span>
- <span style="color:green">Logging with each tasks</span>
- <span style="color:green">Co-located <b>ansible.cfg</b> for more control</span>
- <span style="color:green">Easy to <b>plug-in</b> new custom roles</span>
<br></br>

<table border="1">
    <thead>
        <tr>
            <th>#</th>
            <th>Playbook Name</th>
            <th>Description</th>
            <th>Options / Additional Information</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>01</td>
            <td><a href='./playbook_install_client_redhat.yml'>playbook_install_client_redhat.yml</a></code></td>
            <td rowspan=2>This playbook goes through sequence of tasks defined within each role to perform fresh install or upgrade to the proposed version on the target host machine. The NetBackup Client is installed based on the successful execution of each role described in Roles section. <br> <b><u> High level workflow and capabilities - </u></b> <br> &emsp; - Platform compatibility :- <br> &emsp;&emsp; 1. Checks ansible distribution os family (RedHat) and version(7/8/9). <br> &emsp;&emsp; 2. Checks native dependent packages and installs them if found missing. <br> &emsp;&emsp; 3. Creates required soft-link of native dependent libraries if required. <br> &emsp; - Runs a defensive check and exits if the given target host is a NetBackup Primary/Media server. <br> &emsp; - Validates if the target host is at the desired state to either perform installation/upgrade. <br> &emsp; - If matches the desired state, performs installation/upgrade. <br> &emsp; - If any, NetBackup Client EEB list is provided, installs them and creates individual RPM marker entry for each EEB.</td>
            <td rowspan=4>Client - RedHat</td>
        </tr>
        <tr>
            <td>02</td>
            <td><a href='./playbook_upgrade_client_redhat.yml'>playbook_upgrade_client_redhat.yml</a></td>
        </tr>
        <tr>
            <td>03</td>
            <td><a href='./playbook_remove_client_redhat.yml'>playbook_remove_client_redhat.yml</a></td>
            <td>This playbook goes through sequence of tasks defined within each role to remove specified NetBackup Client version from the target host. <br> <b><u> High level workflow and capabilities - </u></b> <br> &emsp; - Runs a defensive check and exits if the given target host is a NetBackup Primary/Media server. <br> &emsp; - Perform version check and proceed only if specified version is found installed. <br> &emsp; - Removes NetBackup Client footprint on the target host. <br> &emsp; - If any, NetBackup Client EEB RPM Marker is found, removes it.</td>
        </tr>
        <tr>
            <td>04</td>
            <td><a href='./playbook_cert_management_redhat.yml'>playbook_cert_management_redhat.yml</a></td>
            <td>This playbook handles security configuration to establish connection between NetBackup primary server and respective Clients. This playbook could be used when there is a need to relocate client to different primary server or as a disaster recovery options. <br> <b><u> High level workflow and capabilities - </u></b> <br> &emsp; - Runs a defensive check and exits if the given target host is a NetBackup Primary/Media server. <br> &emsp; - Perform version check and proceed only if specified version is found installed. <br> &emsp; - Use the security specifications provided as part of vars to fetch the certificates.</td>
        </tr>
    </tbody>
</table>

## Roles
#### These roles are the integral part of different playbooks and gets called based on the required workflow. Modification or sequencing is not required for the above supported use cases.
<details>
<summary> <b><u><span style="color:#0969DA">Expand to find more details about roles</span></u></b> </summary>

| # | Role Name | Role Description |
| --- | --- |--- |
| 01 | `netbackup/redhat` | Contains static playbook specifications required for different workflows |
| 02 | `generic/os_compatibility` | Verify the OS compatibility for all the supported NetBackup versions. It also installs system dependent packages, if missing. |
| 03 | `generic/server_check` | Performs preventive check to validate whether the target host machine is not a Primary or Media server |
| 04 | `generic/nbu_version_check` | Validates that the given proposed version (`nbu_version`) is supported or not. |
| 05 | `generic/client_check` | Reads the installed NetBackup Client version |
| 06 | `netbackup/redhat/nbu-client-install` | NetBackup Client is installed/upgraded based on the below conditions :- <br> New Install: <br> - No NetBackup Client is installed <br> - Proposed NetBackup Client is installed <br> Upgrade: <br> - Older version of NetBackup Client is installed <br> - Proposed NetBackup Client is installed |
| 07 | `netbackup/redhat/nbu-install-eeb` | Installs the list of EEBs provided as part of initial configuration and creates a RPM marker if FTO `include_eeb_rpm_marker` is set to `true`  |
| 08 | `netbackup/redhat/client-get-certificate` | Performs certificate management of Client installation |
| 09 | `netbackup/redhat/nbu-client-remove` | Removes NetBackup Client only if proposed version is found installed |
</details>
<br>

## Variables
 
#### This [`<playbook_dir>/vars/main.yml`](./vars/main.yml) is user-centric var file and has to be refurbished based on your environment. It contains all the inputs required globally. For all different types of vars, refer below.

<h3><i><u>Mandatory</u></i></h3>

<table border="1">
    <thead>
        <tr>
            <th>#</th>
            <th>Input Variable (<span style="color:red">* - mandatory</span>)</th>
            <th>Description</th>
            <th>Variable Type</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>01</td>
            <td><span style="color:red">*</span><code>nbu_version</code></td>
            <td>Desired NetBackup Client Version to use in the format [x.x.x.x]<br><b>Required</b>:&nbsp;<code>Yes</code><br><b>Format</b>:&nbsp;<code>x.x.x.x</code></td>
            <td>string</td>
        </tr>
        <tr>
            <td>02</td>
            <td><span style="color:red">*</span><code>nbu_artifactory_repo_base_url</code></td>
            <td>Contains the base url to NetBackup yum repository<br><b>Required</b>:&nbsp;<code>Yes</code><br><b>Default</b>:&nbsp;<code>N/A</code></td>
            <td>url</td>
        </tr>
        <tr>
            <td>03</td>
            <td><span style="color:red">*</span><code>nbu_path_repo_base_pkg</code></td>
            <td>Contains path appended to base url for NetBackup yum repository<br><b>Required</b>:&nbsp;<code>Yes</code><br><b>Default</b>:&nbsp;<code>N/A</code></td>
            <td>url</td>
        </tr>
        <tr>
            <td>04</td>
            <td><code>nbu_path_repo_client_eeb_pkg</code></td>
            <td>Contains relative path of EEB installer 
            file<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>N/A</code></td>
            <td>url</td>
        </tr>
        <tr>
            <td>05</td>
            <td><span style="color:red">*</span><code>nbu_primary_server_ans</code></td>
            <td>You must specify the Primary Server hostname in case it's not determined, we can continue with dummy server name as given below<br><b>Required</b>:&nbsp;<code>Yes</code><br><b>Default</b>:&nbsp;<code>PRIMARY01</code></td>
            <td>string</td>
        </tr>
    </tbody>        
</table>

<h3><i><u>Configurable Options</u></i></h3>

<table border="1">
    <thead>
        <tr>
            <th>#</th>
            <th>Input Variable</th>
            <th>Description</th>
            <th>Variable Type</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>01</td>
            <td><code>nbu_primary_certdetails</code><br>&emsp;This var is mutually inclusive to <br>&emsp;<b>FTO</b> : <code>nbu_cert_management</code> </td>
            <td id="nbu_primary_certdetails">You need to provide certificate specification in below JSON format.<br><code>- hostname:'PRIMARY01'</code><br><code>&emsp;&emsp;nbu_server_fingerPrint:'[Primary SHA-1 fingerprint]'</code><br><code>&emsp;&emsp;nbu_server_authorization_token:'[Token Value for Primary]'</code></td>
            <td>JSON</td>
        </tr>       
        <tr>
            <td>02</td>
            <td><code>nbu_eeb_ordered</code></td>
            <td>You can specify list of EEBs to be installed as per Client and NetBackup version<br><code>client:</code><br>&emsp;<code>[NB Version]:</code><br>&emsp;&emsp;<code>- eeb-installer-name</code></td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>03</td>
            <td><code>os_path_nbu_install</code></td>
            <td>Typically NetBackup Client installs on <code>/usr/openv</code>.<br> Update { os_path_nbu_install } in case you want to install on a custom path. We recommend that given path ends with openv, as it gets removed at the time of uninstall.&nbsp;This will make sure that we remove only the NetBackup installed directories.<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>/usr/openv</code></td>
            <td>string</td>
        </tr>
        <tr>
            <td>04</td>
            <td><code>nbu_directory_list_to_be_removed</code></td>
            <td>List of directories which would get removed upon uninstalling NetBackup Client</td>
            <td>list</td>
        </tr>
        <tr>
            <td>05</td>
            <td><code>os_rhel_system_packages</code></td>
            <td>You can add your own OS dependent packages in the list of packages given as per OS versions</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>06</td>
            <td><code>os_rhel_system_packages_symlink</code></td>
            <td>You can add your own OS symlinks in the list of symbolic links given as per OS versions</td>
            <td>JSON</td>
        </tr>
    </tbody>        
</table>

<h3><i><u>Feature Toggle Options (FTO)</u></i></h3>

<table border="1">
    <thead>
        <tr>
            <th>#</th>
            <th>Input Variable</th>
            <th>Description</th>
            <th>Variable Type</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>01</td>
            <td><code>include_eeb_rpm_marker</code></td>
            <td>Feature toggle option to decide whether you want the feature of EEB RPM marker creation. If set to true, EEB RPM marker is created along with EEB installation<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>false</code></td>
            <td>bool</td>
        </tr>
        <tr>
            <td>02</td>
            <td><code>nb_include_java_jre_install</code></td>
            <td>Feature toggle option to decide whether to install JAVA/JRE RPM packages<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>false</code></td>
            <td>bool</td>
        </tr>
        <tr>
            <td>03</td>
            <td><code>nbu_cert_management</code></td>
            <td>Feature toggle option to get the certificate of the Certificate Authority (CA) and fetches the host ID-based security certificate from the specified Primary Server. If set to true, make sure to provide authorization details variable <code><a href="#nbu_primary_certdetails">[nbu_primary_certdetails]</a></code><br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>true</code></td>
            <td>bool</td>
        </tr>
    </tbody>        
</table>

## Getting started with NetBackup Ansible playbooks
### Requirements/Pre-requisites

1. We support ansible-core 2.11 onwards.
2. Ansible Automaton Platform is configured and ready to use.
3. Establish a non-interactive connection to all managed nodes/target hosts.
4. Configure an artifact repository manager and upload all the NetBackup RPMs with respective repodata along with it. The repository type could be selected as yum repository.<br>
   All respective NetBackup Client RPMs can be found in `<NB_Package_DIR>/NetBackup_<NB_VERSION>_CLIENTS2/NBClients/anb/Clients/usr/openv/netbackup/client/Linux/RedHat3.10.0`
5. These playbooks assumes that the ansible inventory is pre-populated.

#### Usage
Once all the pre-requisites are met, below steps could be used to run playbooks.

#### Using ansible CLI
> - The playbook execution would not succeed out-of-the-box as it depends upon certain mandatory variables.
> - We have put-up a template containing these mandatory variables (`<playbook_dir>/vars/main.yml`). Do make sure that you go through the <b>[variables section](#variables)</b> and update vars according to your environment's guidelines.<br>
>     - Update `<playbook_dir>/vars/main.yml` directly and save it. This vars file is **already included** in all the playbooks. So, once it is modified, **values will get picked up automatically**.
>     - **Optionally**, as supported by ansible CLI option, you could specify specific variables using **`--extra-vars`** argument as well.
> - Finally, execute `ansible-playbook` CLI from the playbook's directory. For e.g.
>     - If `vars/main.yml` file has been modified locally
>         ```java
>         [user@host ~]$ ansible-playbook playbook_install_client_redhat.yml -l linux -vv
>         ```
>     - If you would like to use `--extra-vars` CLI option
>         ```java
>         [user@host ~]$ ansible-playbook playbook_install_client_redhat.yml -l linux -vv --extra-vars="nbu_version=10.3.0.0 os_path_nbu_install=/usr/openv"
>         ```

#### From within the Ansible Automation Platform
> <span style="color:#cc9900"><b> - At the time of this documentation, AWX is considered as the web-interface to manage the ansible automation platform.</b></span><br>
> - Considering that the AWX is installed and initial configuration is done as follows.
>   - Inventories have been configured and all the target hosts have been added with required credentials
>   - Project is created and sync using one of the supported **Source Control Type**
> - **Templates: -**
>   - AWX templates, also referred to as Ansible Tower Job Templates, are reusable blueprints for automating tasks within the AWX/Ansible Tower platform.
>   - Create the template and specify the project, inventory to use and playbook to run.
>   - If the **`<playbook_dir>/vars/main.yml`** is modified locally to suit your environment, **Variables** filed can be left empty.
>   - If not, you could copy the entire content from *`<playbook_dir>/vars/main.yml`* and paste in the *Variables* section in YAML format. Update the values to suit your environment.
> - Go ahead and launch the required template to start the playbook execution associated with it.
														
## License

### Disclaimer
The information contained in this publication is subject to change without notice. Veritas Corporation makes no warranty of any kind with regard to this manual, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose. Veritas Corporation shall not be liable for errors contained herein or for incidental or consequential damages in connection with the furnishing, performance, or use of this manual.
The software described in this book is furnished under a license agreement and may be used only in accordance with the terms of the agreement.

### Legal Notice
Last updated: 2024-03-27
Copyright © 2024 Veritas Technologies LLC. All rights reserved. 
Veritas, the Veritas Logo, Veritas Alta, and NetBackup are trademarks or registered trademarks 
of Veritas Technologies LLC or its affiliates in the U.S. and other countries. Other names may 
be trademarks of their respective owners. 
This product may contain third-party software for which Veritas is required to provide attribution 
to the third party (“Third-party Programs”). Some of the Third-party Programs are available 
under open source or free software licenses. The License Agreement accompanying the 
Software does not alter any rights or obligations you may have under those open source or 
free software licenses. Refer to the Third-party Legal Notices document accompanying this 
Veritas product or available at: 
https://www.veritas.com/about/legal/license-agreements 
The product described in this document is distributed under licenses restricting its use, copying, 
distribution, and decompilation/reverse engineering. No part of this document may be 
reproduced in any form by any means without prior written authorization of Veritas Technologies 
LLC and its licensors, if any. 
THE DOCUMENTATION IS PROVIDED "AS IS" AND ALL EXPRESS OR IMPLIED 
CONDITIONS, REPRESENTATIONS AND WARRANTIES, INCLUDING ANY IMPLIED 
WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR 
NON-INFRINGEMENT, ARE DISCLAIMED, EXCEPT TO THE EXTENT THAT SUCH 
DISCLAIMERS ARE HELD TO BE LEGALLY INVALID. Veritas Technologies LLC SHALL 
NOT BE LIABLE FOR INCIDENTAL OR CONSEQUENTIAL DAMAGES IN CONNECTION 
WITH THE FURNISHING, PERFORMANCE, OR USE OF THIS DOCUMENTATION. THE 
INFORMATION CONTAINED IN THIS DOCUMENTATION IS SUBJECT TO CHANGE 
WITHOUT NOTICE. 
The Licensed Software and Documentation are deemed to be commercial computer software 
as defined in FAR 12.212 and subject to restricted rights as defined in FAR Section 52.227-19 
"Commercial Computer Software - Restricted Rights" and DFARS 227.7202, et seq. 
"Commercial Computer Software and Commercial Computer Software Documentation," as 
applicable, and any successor regulations, whether delivered by Veritas as on premises or 
hosted services. Any use, modification, reproduction release, performance, display or disclosure 
of the Licensed Software and Documentation by the U.S. Government shall be solely in 
accordance with the terms of this Agreement. 

Veritas Technologies LLC 
2625 Augustine Drive 
Santa Clara, CA 95054 

### Third-Party Legal Notices
Veritas offerings may include third-party materials that are subject to a separate license. Those materials are specified in a Third-party Notices document which may either be posted below on this site and/or included in the ReadMe file or Documentation for the applicable offering.
