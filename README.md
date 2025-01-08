# NetBackup Automation Platform

## Description

Veritas NetBackup is the most powerful and widely adopted data protection solution in the world. NetBackup streamlines data protection management, protects your enterprise from the unforeseen, ensures business-critical resilience and delivers customer choice with a single platform supporting any workload, cloud and architecture at any scale.
The project contains Ansible roles and playbooks for automating the deployment and configuration of NetBackup. The roles and the playbooks are provided in order to demonstrate the automated NetBackup tasks and leverage NetBackup APIs in an automation workflow.<br>

> <span style="color:#0000ff"><b>NOTE:- </b></span> These playbooks support below NetBackup Client/Media/Primary versions.<br>
> * <span style="color:#cc9900"><b>10.5.0.0</b></span><br>
> * <span style="color:#cc9900"><b>10.4.0.1</b></span><br>
> * <span style="color:#cc9900"><b>10.4.0.0</b></span><br>
> * <span style="color:#cc9900"><b>10.3.0.1</b></span><br>
> * <span style="color:#cc9900"><b>10.3.0.0</b></span><br>
> * <span style="color:#cc9900"><b>10.2.0.1</b></span><br>
> * <span style="color:#cc9900"><b>10.1.1.0</b></span><br>
> * <span style="color:#cc9900"><b>10.1.0.0</b></span><br>
> * <span style="color:#cc9900"><b>10.0.0.1</b></span><br>
> * <span style="color:#cc9900"><b>10.0.0.0</b></span><br>

## Project Contents

This project contains Ansible playbooks, roles, vars for automating various deployment tasks for <b>NetBackup Media, Primary & Client</b>. We support below functionalities with our ansible playbooks:
- Fresh installation of NB Client on Windows/SuSE/RHEL.

- Fresh installation of NetBackup Media & Primary on SuSE/RHEL.
- Upgrade NetBackup <b>[to and from NB version 10.x].</b>
- Independent certificate deployment, could be used when :-
  - <i>Certificate deployment wasn't done at the first time with installation
  - Addition of new primary server</i>
- Removal of NetBackup Client, Media & Primary.
- EEB Management with deployment of NetBackup. It does create EEB marker at the standard RPM (Linux) and MSI (Windows) database for easy detection.
  - <i>One or more EEBs could be installed together
  - Upgrade EEBs
  - Adjust subsequent overlapping EEBs
  - Removal of EEBs</i>
- Staging NetBackup Packages Locally
  - <i>If required, this playbook could be used to cache NB pkgs locally on the target host. Later it would get used for offline installation</i>
- Apply Global Security Settings
  - <i> If required, this playbook could be used for applying the global security settings </i>
- Playbook to Start, Stop, Restart NetBackup Services

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
            <th>NetBackup Product</th>
            <th>Operating System</th>
            <th>Playbook Name</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>01</td>
            <td rowspan=6>Client</td>
             <td rowspan=6>1.Linux(Rhel/SuSE)<br>2. Windows</td>
            <td><a href='./playbook_install_client_linux.yml'>playbook_install_client_linux.yml</a></code></td>
            <td rowspan=4>This playbook goes through sequence of tasks defined within each role to perform fresh install or upgrade to the proposed version on the target host machine. The NetBackup Client is installed based on the successful execution of each role described in Roles section. <br> <b><u> High level workflow and capabilities - </u></b> <br> &emsp; - Platform compatibility :- <br> &emsp;&emsp; 1. Checks ansible distribution os family and version. <br> &emsp;&emsp; 2. Checks native dependent packages and installs them if found missing. <br> &emsp;&emsp; 3. Creates required soft-link on linux of native dependent libraries if required. <br> &emsp; - Runs a defensive check and exits if the given target host is a NetBackup Primary/Media server. <br> &emsp; - Validates if the target host is at the desired state to either perform installation/upgrade. <br> &emsp; - If matches the desired state, performs installation/upgrade. <br> &emsp; - If FTO <a href="#nbu_cert_management">[nbu_cert_management]</a> is set to true, deploy certificates based on primary server CA usage.
            <br> &emsp; - At different stages, we perform connectivity validation with given Primary server. <br> &emsp; - If any, NetBackup Client EEB list is provided, installs them and creates individual marker entry for each EEB.</td>
        </tr>
        <tr>
            <td>02</td>
            <td><a href='./playbook_upgrade_client_linux.yml'>playbook_upgrade_client_linux.yml</a></td>
        </tr>
        <tr>
            <td>03</td>
            <td><a href='./playbook_install_client_windows.yml'>playbook_install_client_windows.yml</a></td>
        </tr>
        <tr>
            <td>04</td>
            <td><a href='./playbook_upgrade_client_windows.yml'>playbook_upgrade_client_windows.yml</a></td>
        </tr>
        <tr>
            <td>05</td>
            <td><a href='./playbook_remove_client_linux.yml'>playbook_remove_client_linux.yml</a></td>
            <td rowspan=2>This playbook goes through sequence of tasks defined within each role to remove specified NetBackup Client version from the target host. <br> <b><u> High level workflow and capabilities - </u></b> <br> &emsp; - Runs a defensive check and exits if the given target host is a NetBackup Primary/Media server. <br> &emsp; - Perform version check and proceed only if specified version is found installed. <br> &emsp; - Removes NetBackup Client footprint on the target host. <br> &emsp; - If any, NetBackup Client EEB Marker is found, removes it.</td>
        </tr>
        <tr>
            <td>06</td>
            <td><a href='./playbook_remove_client_windows.yml'>playbook_remove_client_windows.yml</a></td>
        </tr>
        <tr>
            <td>07</td>
            <td rowspan=6>Server(Primary/Media)</td>
            <td rowspan=6>Linux(Rhel/SuSE)</td>
            <td><a href='./playbook_install_media_linux.yml'>playbook_install_media_linux.yml</a></code></td>
            <td rowspan=4>This playbook goes through sequence of tasks defined within each role to perform fresh install or upgrade to the proposed version on the target host machine. The NetBackup Media/Primary is installed based on the successful execution of each role described in Roles section. <br> <b><u> High level workflow and capabilities - </u></b> <br> &emsp; - Platform compatibility :- <br> &emsp;&emsp; 1. Checks ansible distribution os family and version. <br> &emsp;&emsp; 2. Checks native dependent packages and installs them if found missing. <br> &emsp;&emsp; 3. Creates required soft-link on linux of native dependent libraries if required.<br> &emsp;&emsp; 4. Perform space check for remote host machine. If remote machine doesn't have sufficient for install/upgrade. it exists with proper custom error message. <br> &emsp; - Runs a defensive check and exits if the given target host is a NetBackup Primary/Client server. <br> &emsp; - Runs a defensive check and exits if the proposed netbackup media/primary version is not supported. <br> &emsp; - Validates if the target host is at the desired state to either perform installation/upgrade. <br> &emsp; - If matches the desired state, performs installation/upgrade. <br> &emsp; - For Primary, ITA Data Collector is installed/upgraded based on <code>do_install_ita_dc</code> option. <br> &emsp; - If FTO <a href="#nbu_cert_management">[nbu_cert_management]</a> is set to true, deploy certificates based on primary server CA usage.
            <br> &emsp; - For media at different stages, we perform connectivity validation with given Primary server.<br> &emsp; - If any, NetBackup Media/Primary EEB list is provided, installs them and creates individual RPM marker entry for each EEB.</td>
        </tr>
        <tr>
            <td>08</td>
            <td><a href='./playbook_upgrade_media_linux.yml'>playbook_upgrade_media_linux.yml</a></td>
        </tr>
        <tr>
            <td>09</td>
            <td><a href='./playbook_install_primary_linux.yml'>playbook_install_primary_linux.yml</a></td>
        </tr>
        <tr>
            <td>10</td>
            <td><a href='./playbook_upgrade_primary_linux.yml'>playbook_upgrade_primary_linux.yml</a></td>
        </tr>
        <tr>
            <td>11</td>
            <td><a href='./playbook_remove_media_linux.yml'>playbook_remove_media_linux.yml</a></code></td>
            <td rowspan=2>This playbook goes through sequence of tasks defined within each role to remove specified NetBackup Server(Primary/Media) version from the target host. <br> <b><u> High level workflow and capabilities - </u></b>  <br> &emsp; - Runs a defensive check and exits if the given target host has different NetBackup role.<br> &emsp; - Perform version check and proceed only if specified version is found installed. <br> &emsp; - Removes NetBackup Primary/Media footprint on the target host. <br> &emsp; - If ITA Data Collector if found, removes it. <br> &emsp; - If any, NetBackup Primary/Media EEB RPM Marker is found, removes it.</td>
        </tr>
        <tr>
            <td>12</td>
            <td><a href='./playbook_remove_primary_linux.yml'>playbook_remove_primary_linux.yml</a></td>
        </tr>
        <tr>
            <td>13</td>
             <td rowspan=8>Common</td>
             <td rowspan=8>1.Linux(Rhel/SuSE)<br>2.Windows</td>
            <td ><a href='./playbook_certificate_deployment_linux.yml'>playbook_certificate_deployment_linux.yml</a></td>
            <td rowspan=2>This playbook handles security configuration to establish connection between NetBackup primary server and respective Clients/Media. This playbook could be used <br> - when there is a need to add new primary server onto client/media. <br> - when there is need to enroll external certificate authority with primary server. <b><u> High level workflow and capabilities - </u></b> <br> &emsp; - For media server playbooks it runs a defensive check and exits if the given target host is a NetBackup Primary. <br> &emsp; - Perform version check and proceed only if specified version is found installed. <br> &emsp; - If FTO <a href="#nbu_cert_management">[nbu_cert_management]</a> is set to true, use the security specifications (NBCA/ECA) provided as part of vars given below:<br>&emsp;&emsp; <a href="#nbu_eca_certdetails">[nbu_eca_certdetails]</a>- To configure a host to use an external signed certificate. <br>&emsp;&emsp; <a href="#nbu_primary_certdetails">[nbu_primary_certdetails]</a>- To configure a host to use NetBackup CA signed certificate. </td>
        </tr>
        <tr>
            <td>14</td>
            <td><a href='./playbook_certificate_deployment_windows.yml'>playbook_certificate_deployment_windows.yml</a></td>
        </tr>
        <tr>
            <td>15</td>
            <td><a href='./playbook_stage_packages_locally_redhat.yml'>playbook_stage_packages_locally_redhat.yml</a></td>
            <td rowspan=2>This playbook goes through sequence of tasks defined within each role to download NetBackup rpm or DVD packages locally. <br> <b><u> High level workflow and capabilities - </u></b> 
            <br> &emsp; - Validate if the proposed netbackup version is supported. 
            <br> &emsp; - For Linux, downloads the package to local YUM repo cache.
            <br> &emsp; - For Windows, downloads the package to local temp.
            <br> &emsp;&emsp;
            </td>
        </tr>
        <tr>
            <td>16</td>
            <td><a href='./playbook_stage_packages_locally_windows.yml'>playbook_stage_packages_locally_windows.yml</a></td>
        </tr>
        <tr>
            <td>17</td>
            <td><a href='./playbook_configuration_global_settings.yml'>playbook_configuration_global_settings.yml</a></td>
            <td rowspan=1>This playbook is to update Global Security Settings to enhance secure communications.
            </td>
        </tr>
        <tr>
            <td>18</td>
            <td><a href='./playbook_start_services_linux.yml'>playbook_start_services_linux.yml</a></td>
            <td rowspan=3>This playbook is used for start, stop and restart all the NetBackup services.
            </td>
        </tr>
        <tr>
            <td>19</td>
            <td><a href='./playbook_stop_services_linux.yml'>playbook_stop_services_linux.yml</a></td>
        </tr>
        <tr>
            <td>20</td>
            <td><a href='./playbook_restart_services_linux.yml'>playbook_restart_services_linux.yml</a></td>
        </tr>
    </tbody>
</table>

## Roles
#### These roles are the integral part of different playbooks and gets called based on the required workflow. Modification or sequencing is not required for the above supported use cases.
<details>
<summary> <b><u><span style="color:#0969DA">Expand to find more details about roles</span></u></b> </summary>

| # | Role Name (generic) | Role Description(Immutable operations to perform validation or system checks) |
| --- | --- |--- |
| 01 | `generic/initiate_nbcheck` | Run NBCheck before install/upgrade of NetBackup. This role will get called only if FTO `include_nbu_nbcheck` is set to `true` |
| 02 | `generic/is_nbu_version_supported` | Validates that the given proposed version (`nbu_version`) is supported or not. |
| 03 | `generic/nbu_compatibility` | Perform preventive check to validate NetBackup installed or not. Check the installed version of NetBackup is compatible with the NetBackup Primary server version |
| 04 | `generic/nbu_space_check` | Validate that remote machine has sufficient space for install/upgrade of NetBackup |
| 05 | `generic/nbu_verification` | validate the certificate-specific configurations |
| 06 | `generic/os_compatibility` | Verify the OS compatibility for all the supported NetBackup versions. It also installs system dependent packages, if missing. |


| # | Role Name (helper) | Role Description (It contains helper functions which required for generic and netbackup roles ...) |
| --- | --- |--- |
| 01 | `helper/nbu_role_status` | "Performs preventive check to validate whether the target host machine is not a Primary or Media server" |
| 02 | `helper/nbu_version_installed` | Reads the installed NetBackup version |
| 03 | `helper/detect_partial_install` | Detect the partial installation state |

| # | Role Name (netbackup) | Role Description (Performs system level changes which includes installation, uninstallation, removal, etc ...) |
| --- | --- |--- |
| 01 | `netbackup/common/nbu-get-certificate` | This role initially checks Certificate mode of Primary Server, depending on that what mode we receive from primary(NBCA/ECA) performs certificate deployment of Client/Media installation. |
| 02 | `netbackup/common/stage-package-locally` | Staging playbook to download netbackup packages into local cache and use it during install-time. |
| 03 | `netbackup/linux` <br> `netbackup/win32nt`</br> | Contains static playbook specifications required for different workflows |
| 04 | `netbackup/linux/nbu-client-install` <br> `netbackup/linux/nbu-server-install` <br> `netbackup/win32nt/nbu-client-install`  | NetBackup Client/Media/Primary is installed/upgraded based on the below conditions :- <br> New Install: <br> - No NetBackup Client/Media/Primary is installed <br> - Proposed NetBackup Client/Media/Primary is installed <br> Upgrade: <br> - Older version of NetBackup Client/Media/Primary is installed <br> - Proposed NetBackup Client/Media/Primary is installed |
| 05 | `netbackup/linux/nbu-install-eeb`<br>`netbackup/win32nt/nbu-install-eeb` | Installs the list of EEBs provided as part of initial configuration and creates a marker if FTO `include_eeb_rpm_marker` is set to `true`  |
| 06 | `netbackup/linux/nbu-remove` <br> `netbackup/win32nt/nbu-remove`</br> | Removes NetBackup Client/Primary/Media only if proposed version is found installed |
| 07 | `netbackup/linux/nbu-stop-services` | This role deals with nbu service moves NetBackup only if proposed version is found installed
| 08 | `netbackup/linux/symlink-operations` | This role deals with validation and creation of symlink on linux. |
| 09 | `netbackup/linux/nbu-install-verification` | This role deals with below validation.<br> - Check NetBackup installed or not and depend on it set the installation status to install/none<br> - Check installed NetBackup version is less than proposed version and need upgrade. Set install status to upgrade, if upgrade it required<br> - If current version is equal to proposed version it set install status to none |
| 10 | `netbackup/common/rest-api-integration` | This role included the global security setting for configuring the secure communications.<br>   |
| 11 | `netbackup/linux/nbu-start-services` <br> `netbackup/linux/nbu-stop-services` <br> | This role deals with starting and stopping the NetBackup services |
| 12 | `netbackup/linux/pre-install-os-task` <br> | This role handles the pre installation os tasks for Primary. We validate the specified user name and groups, create local users/groups if missing |
</details>
<br>

## Variables
 
#### This [`<playbook_dir>/vars/linux.yml`](./vars/linux.yml) and [`<playbook_dir>/vars/win32nt.yml`](./vars/win32nt.yml) is user-centric var file and has to be refurbished based on your environment. It contains all the inputs required globally. For all different types of vars, refer below.

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
            <td>Desired NetBackup Version to use in the format [x.x.x.x]<br><b>Required</b>:&nbsp;<code>Yes</code><br><b>Format</b>:&nbsp;<code>x.x.x.x</code></td>
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
        <tr>
            <td>06</td>
            <td><span style="color:red">*</span><code>nbu_cust_reg_file_name</code></td>
            <td>You must specify the usage insights customer registration key file valid for nbu_version&nbsp;<code><= "10.2.0.1"</code> primary server installation/upgrade.<br><b>Required</b>:&nbsp;<code>Yes, For primary server</code><br><b>Default</b>:&nbsp;<code>""</code></td>
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
            <td id="nbu_primary_certdetails">If the primary server is using only NBCA, target host is configured using NBCA. In this case hostname, nbu_server_fingerPrint and nbu_server_authorization_token values are required. You need to provide configuration options for NetBackup CA-signed certificates in below JSON format.<br><code>- hostname:'PRIMARY01'</code><br><code>&emsp;&emsp;nbu_server_fingerPrint:'[Primary SHA-1 fingerprint]'</code><br><code>&emsp;&emsp;nbu_server_authorization_token:'[Token Value for Primary]'</code></td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>02</td>
            <td><code>nbu_eca_certdetails[Linux]</code><br>&emsp;This var is mutually inclusive to <br>&emsp;<b>FTO</b> : <code>nbu_cert_management</code> </td>
            <td id="nbu_eca_certdetails">If the primary server is configured to use external certificate authority (ECA) or mixed mode (NBCA & ECA), target host would have to be configured with ECA.<br> In this case, provide input to below fields. <br><code><span style="color:red">*</span>nbu_eca_cert_path:''</code><br><code><span style="color:red">*</span>nbu_eca_private_key_path:''</code><br><code><span style="color:red">*</span>nbu_eca_trust_store_path:''</code><br><code>nbu_eca_key_passphrasefile:'[ If the private key of the external certificate is encrypted,nbu_eca_key_passphrasefile is required ]'</code><br><code>eca_crl:</code><br><code>&emsp;&emsp;nbu_eca_crl_check_level:'[ Valid options are 'USE_CDP', 'USE_PATH', 'DISABLED' ]'</code><br><code>&emsp;&emsp;nbu_eca_crl_path:'[ Required only when nbu_eca_crl_check_level = USE_PATH ]'</code></td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>02</td>
            <td><code>nbu_eca_certdetails[Windows]</code><br>&emsp;This var is mutually inclusive to <br>&emsp;<b>FTO</b> : <code>nbu_cert_management</code> </td>
            <td id="nbu_eca_certdetails">Similarly on Windows when the primary server is configured to use external certificate authority (ECA) or mixed mode (NBCA & ECA), target host would have to be configured with ECA. Here we support both file based certificates and Windows Certificate Store.<br>In both cases, provide input to relevant fields as per certificate store type.<br><code>cert_store_type:'[ Options are ['windows_cert_store', 'windows_file_based']]'</code><br><code>windows_cert_store:</code><br><code>&emsp;&emsp;<span style="color:red">*</span>nbu_eca_cert_location:''</code><br><code>windows_file_based:</code><br><code>&emsp;&emsp;<span style="color:red">*</span>nbu_eca_cert_path:''</code><br><code>&emsp;&emsp;<span style="color:red">*</span>nbu_eca_private_key_path:''</code><br><code>&emsp;&emsp;<span style="color:red">*</span>nbu_eca_trust_store_path:''</code><br><code>&emsp;&emsp;nbu_eca_key_passphrasefile:'[ If the private key of the external certificate is encrypted,nbu_eca_key_passphrasefile is required ]'</code><br><code>eca_crl:</code><br><code>&emsp;&emsp;nbu_eca_crl_check_level:'[ Valid options are 'USE_CDP', 'USE_PATH', 'DISABLED' ]'</code><br><code>&emsp;&emsp;nbu_eca_crl_path:'[ Required only when nbu_eca_crl_check_level = USE_PATH ]'</code></td>
            <td>JSON</td>
        </tr>        
        <tr>
            <td>03</td>
            <td><code>nbu_eeb_ordered</code></td>
            <td>You can specify list of EEBs to be installed as per NetBackup version<br><code>client:</code><br>&emsp;<code>[NB Version]:</code><br>&emsp;&emsp;<code>- eeb-installer-name</code>
                        <br><code>media:</code><br>&emsp;<code>[NB Version]:</code><br>&emsp;&emsp;<code>- eeb-installer-name</code>
            <br><b>Examples based on different use cases :-</b><br><b>1.</b> For upgrading EEB from old version to new version. We need to first uninstall old EEB with -uninstall flag and then install new EEB.</br>&emsp;&emsp;<b>Eg.</b> In order to upgrade EEB_XXXXX_1 to EEB_XXXXX_15, we would have to specify both the EEBs in the ordered list as follows:</b><br>&emsp;<code>client:</code><br>&emsp;&emsp;<code>10.1.1.0:</code><br>&emsp;&emsp;&emsp;<code>- "EEB_XXXXX_1 -uninstall"</code></code><br>&emsp;&emsp;&emsp;<code>- "EEB_XXXXX_15"</code>
            <br><b>2.</b> In case of overlapping EEBs, If we have <b>EEB_xxxxx_x</b> which is bundled EEB of <br><code>['EEB_X1', 'EEB_X2', 'EEB_X3']</code>
            <br>If user wants to install <b>EEB_XXXX2_12</b> which overlaps above <b>EEB_X2</b>. It means  EEB_XXXX2_12 can't be installed unless overlapping EEB_X2 is removed. So to install EEB_XXXX2_12, first we need to uninstall overlapped EEB_X2 with -uninstall flag and then install EEB_XXXX2_12 as shown below:
            <br>&emsp;<code>client:</code><br>&emsp;&emsp;<code>10.1.1.0:</code><br>&emsp;&emsp;&emsp;<code>- "EEB_XXXXX_x"</code><br>&emsp;&emsp;&emsp;<code>- "EEB_X2 -uninstall"</code><br>&emsp;&emsp;&emsp;<code>- "EEB_XXXX2_12"</code>
            <br><b>3.</b>In order to uninstall certain EEB's which was already installed. We can uninstall EEB's with -uninstall flag as shown below.<br><b>Eg.</b><br>&emsp;<code>client:</code><br>&emsp;&emsp;<code>10.1.1.0:</code><br>&emsp;&emsp;&emsp;<code>- "eebinstaller_XXXX1_X -uninstall"</code></code><br>&emsp;&emsp;&emsp;<code>- "eebinstaller_XXXX2_X -uninstall"</code>
            <br><b>4.</b>At times, certain EEBs need to be executed with special arguments like <code>-create</code>. You just need to specify the arguments along with EEB name in the ordered list. <br><b>Eg.</b><br>&emsp;<code>client:</code><br>&emsp;&emsp;<code>10.1.1.0:</code><br>&emsp;&emsp;&emsp;<code>- "eebinstaller_XXXX1_X -create"</code></code><br>&emsp;&emsp;&emsp;<code>- "eebinstaller_XXXX2_X"</code></td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>04</td>
            <td><code>os_path_nbu_install</code></td>
            <td>Typically NetBackup installs on <code>/usr/openv</code> for Linux and <code>C:\Program Files\Veritas</code> for Windows.<br> Update { os_path_nbu_install } in case you want to install on a custom path. We recommend that given path ends with openv on Linux and Veritas on windows, as it gets removed at the time of uninstall.&nbsp;This will make sure that we remove only the NetBackup installed directories.            <br><code>Linux:</code><br>&emsp;</code><b>Default</b>:&nbsp;<code>/usr/openv</code>
            <br><code>Windows:</code><br>&emsp;</code><b>Default</b>:&nbsp;<code>C:\Program Files\Veritas</code></td>
            <td>string</td>
        </tr>
        <tr>
            <td>05</td>
            <td><code>nbu_directory_list_to_be_removed</code></td>
            <td>List of directories which would get removed upon uninstalling NetBackup</td>
            <td>list</td>
        </tr>
        <tr>
            <td>06</td>
            <td><code>os_rhel_system_packages</code></td>
            <td>You can add your own OS dependent packages in the list of packages given as per OS versions</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>07</td>
            <td><code>os_rhel_system_packages_symlink</code></td>
            <td>You can add your own OS symlinks in the list of symbolic links given as per OS versions</td>
            <td>JSON</td>
        </tr>
        <tr>
            <td>08</td>
            <td><code>nbu_license_key</code></td>
            <td>In case of media install/upgrade. You must specify NBU license key for <code>nbu_version == 10.0.0.1 and nbu_version == 10.0.0.0</code><br><b>Default</b>:&nbsp;<code>""</code></td>
            <td>list</td>
        </tr>
         <tr>
            <td>09</td>
            <td><code>nbu_license_file_name_list</code></td>
            <td>In case of primary install/upgrade. You must specify NBU license file for <code>nbu_version >= 10.2.0.1</code><br>&emsp;<code>nbu_license_file_name_list:</code><br>&emsp;&emsp;<code>- "<<slic_filepath1>>"</code><br>&emsp;&emsp;<code>- "<<slic_filepath1>>"</code></code></td>
            <td>list</td>
        </tr>
         <tr>
            <td>10</td>
            <td>nbu_webservices_group: <code>nbwebgrp</code></td>
            <td rowspan=5>We validate the specified user name and groups, create local users/groups if missing 
            <td rowspan=5>string</td>
        </tr>
         <tr>
            <td>11</td>
            <td>nbu_webservices_user:<code>nbwebsvc</code></td>
        </tr>
         <tr>
            <td>12</td>
            <td><code>nbu_services_group</code></td>
        </tr>
         <tr>
            <td>13</td>
            <td><code>nbu_services_user</code></td>
        </tr>
        <tr>
            <td>14</td>
            <td><code>nbu_database_user</code></td>
        </tr>
        <tr>
            <td>15</td>
            <td><code>postgresql_pooler_odbc_port</code></td>
            <td>This is an optional var, if not specified, would use default ('13787')
            <br><b>Required</b>:&nbsp;<code>Optional</code><br>
            <td>string</td>
        </tr>
         <tr>
            <td>16</td>
            <td><code>security_properties_params</code></td>
            <td>This var is for global security setting
            <br><code> &emsp;&emsp;certificateAutoDeployLevel: 1</code><br><code>&emsp;&emsp;dteGlobalMode: "PREFERRED_ON"</code><br><code>&emsp;&emsp;allowInsecureBackLevelHost: 0</code><br><code>&emsp;&emsp;aliasAutoAdd: 1</code></td>
            <td>string</td>
        </tr>
        <tr>
            <td>17</td>
            <td><code>setPassphraseConstraintsRequest</code></td>
            <td>This var is for setting the passpharase constraint request
            <br><code> &emsp;&emsp;minPassphraseLength: 18</code><br><code>&emsp;&emsp;minUpperCaseRequired: 1</code><br><code>&emsp;&emsp;minLowerCaseRequired: 1</code></td>
            <td>string</td>
        </tr>
         <tr>
            <td>18</td>
            <td><code>drpkgpassphrase</code></td>
            <td>This var is required for disaster recovery passphrase
            </td>
            <td>string</td>
        </tr>
         <tr>
            <td>19</td>
            <td><code>nbu_db_data_path</code></td>
            <td>This var is required if specify the postgre database user path
            </td>
            <td>string</td>
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
            <td>FTO to decide whether you want the feature of EEB marker creation. If set to true, EEB marker is created along with EEB installation<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>false</code></td>
            <td>bool</td>
        </tr>
        <tr>
            <td>02</td>
            <td><code>nb_include_java_jre_install</code></td>
            <td>FTO to decide whether to install JAVA/JRE RPM packages<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>false</code></td>
            <td>bool</td>
        </tr>
        <tr>
            <td>03</td>
            <td id="nbu_cert_management"><code>nbu_cert_management[NBCA/ECA]</code></td>
            <td><b>[NBCA]</b>FTO to get the certificate of the Certificate Authority (CA) and fetches the host ID-based security certificate from the specified Primary Server. If set to true and primary server is configured to use only NBCA make sure to provide authorization details variable <code><a href="#nbu_primary_certdetails">[nbu_primary_certdetails]</a></code><br><b>[ECA]</b>FTO to get the certificate issued by a CA other than the NetBackup CA and referred to as external CA-signed certificates. Starting 8.2, NetBackup CA-signed host ID-based certificates can be replaced by external CA-signed certificates. If set to true, make sure to provide authorization details variable <code><a href="#nbu_eca_certdetails">[nbu_eca_certdetails]</a></code><br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>true</code></td>
            <td>bool</td>
        </tr>
        <tr>
            <td>04</td>
            <td><code>do_perform_nbcheck_preinstall</code></td>
            <td>FTO to decide whether to run NBCheck before starting install/upgrade<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>true</code></td>
            <td>bool</td>
        </tr>
        <tr>
            <td>05</td>
            <td><code>install_pkgs_from_local_cache</code></td>
            <td>FTO to decide whether to download rpm packages or not. If set to true, packages are cached locally independently or by using staging playbook to avoid downloading the packages at install-time.<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>false</code></td>
            <td>bool</td>
        </tr>
        <tr>
            <td>06</td>
            <td><code>ignore_primary_connectivity_failures</code></td>
            <td>FTO to decide whether to ignore connectivity validation and continue execution. If set to true, It ignores connectivity validation  with primary and continue execution.<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>false</code></td>
            <td>bool</td>
        </tr>
        <tr>
            <td>07</td>
            <td><code>skip_primary_version_compatibility_check</code></td>
            <td>FTO to Skip Primary server version compatibility check. If set to true, It skip Primary server version compatibility check.<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>false</code></td>
            <td>bool</td>
        </tr>
        <tr>
            <td>08</td>
            <td><code>should_force_process_termination</code></td>
            <td>FTO to terminate the processes forcefully. If set to true, After 3 attempts of graceful shutdown, forcefully terminate the running processes.<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>false</code></td>
            <td>bool</td>
        </tr>
        <tr>
            <td>09</td>
            <td><code>do_install_ita_dc</code></td>
            <td>FTO to install ITA Data Collector optional package.<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>true</code></td>
            <td>bool</td>
        </tr>
         <tr>
            <td>10</td>
            <td><code>skip_missing_catalog_backup_check</code></td>
            <td>FTO to skip last 24 hours successful catalog backup check.<br><b>Required</b>:&nbsp;<code>Optional</code><br><b>Default</b>:&nbsp;<code>false</code></td>
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
   <br>
   and All respective NetBackup Media/Primary RPMs can be found in `<NB_Package_DIR>/NetBackup_<NB_VERSION>_LinuxR_x86_64/linuxR_x86/anb`
   <br>
   All respective NetBackup client windows DVD packages can be found in
   `<NB_Package_DIR>/NetBackup_<NB_VERSION>_Win\`
   <br>
   For Primary server, you must upload IT Data Collector package [`<NB_Package_DIR>/NetBackup_<NB_VERSION>_LinuxR_x86_64/linuxR_x86/catalog/anb/ita_dc.tar.gz`] as well.
5. These playbooks assumes that the ansible inventory is pre-populated.

#### Usage
Once all the pre-requisites are met, below steps could be used to run playbooks.

#### Using ansible CLI
> - The playbook execution would not succeed out-of-the-box as it depends upon certain mandatory variables.
> - We have put-up a template containing these mandatory variables (`<playbook_dir>/vars/linux.yml or <playbook_dir>/vars/win32nt.yml`). Do make sure that you go through the <b>[variables section](#variables)</b> and update vars according to your environment's guidelines.<br>
>     - Update `<playbook_dir>/vars/linux.yml` for linux and `<playbook_dir>/vars/win32nt.yml` for windows directly and save it. This vars file is **already included** in all the playbooks. So, once it is modified, **values will get picked up automatically**.
>     - **Optionally**, as supported by ansible CLI option, you could specify specific variables using **`--extra-vars`** argument as well.
> - Finally, execute `ansible-playbook` CLI from the playbook's directory. For e.g.
>     - If `vars/linux.yml` file has been modified locally
>         ```java
>         [user@host ~]$ ansible-playbook playbook_install_client_redhat.yml -l linux -vv
>         ```
>     - If `vars/win32nt.yml` file has been modified locally
>         ```java
>         [user@host ~]$ ansible-playbook playbook_install_client_windows.yml -l win -vv
>         ```
>     - If you would like to use `--extra-vars` CLI option , we recommend to specify in JSON format
>         ```java
>         For Linux:
>         [user@host ~]$ ansible-playbook playbook_install_client_redhat.yml -l linux -vv --extra-vars="nbu_version=10.3.0.0 os_path_nbu_install=/usr/openv"
>         ```
>         ```java
>         For Windows:
>         [user@host ~]$ ansible-playbook playbook_install_client_windows.yml -l win -vv --extra-vars="nbu_version=10.3.0.0 os_path_nbu_install=C:\Program Files\Veritas"
>         ```

#### From within the Ansible Automation Platform
> <span style="color:#cc9900"><b> - At the time of this documentation, AWX is considered as the web-interface to manage the ansible automation platform.</b></span><br>
> - Considering that the AWX is installed and initial configuration is done as follows.
>   - Inventories have been configured and all the target hosts have been added with required credentials
>   - Project is created and sync using one of the supported **Source Control Type**
> - **Templates: -**
>   - AWX templates, also referred to as Ansible Tower Job Templates, are reusable blueprints for automating tasks within the AWX/Ansible Tower platform.
>   - Create the template and specify the project, inventory to use and playbook to run.
>   - If the **`<playbook_dir>/vars/linux.yml or <playbook_dir>/vars/win32nt.yml`** is modified locally to suit your environment, **Variables** filed can be left empty.
>   - If not, you could copy the entire content from *`<playbook_dir>/vars/linux.yml or <playbook_dir>/vars/win32nt.yml`* and paste in the *Variables* section in YAML format. Update the values to suit your environment.
> - Go ahead and launch the required template to start the playbook execution associated with it.
														
## License

### Disclaimer
The information contained in this publication is subject to change without notice. Veritas Corporation makes no warranty of any kind with regard to this manual, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose. Veritas Corporation shall not be liable for errors contained herein or for incidental or consequential damages in connection with the furnishing, performance, or use of this manual.
The software described in this book is furnished under a license agreement and may be used only in accordance with the terms of the agreement.

### Legal Notice
Last updated: 2024-03-27
Copyright © 2025 Veritas Technologies LLC. All rights reserved. 
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