# NetBackup Automation Platform

## 🚀 Overview

The NetBackup Automation Platform provides a robust set of Ansible roles and playbooks designed to automate the deployment, configuration, and management of NetBackup environments. Leveraging NetBackup APIs within automation workflows, this project aims to streamline data protection, enhance business resilience, and provide flexibility across various workloads, clouds, and architectures.

## ✨ Key Features

This platform offers comprehensive automation capabilities for NetBackup Primary, Media, and Client components:

* **NetBackup Installation & Upgrades**:
    * Fresh installation and upgrade of NetBackup Client on Windows, SuSE, RHEL, Solaris, AIX, Linux P-series, Linux Z-series, Rocky Linux, and Oracle Linux.
    * Fresh installation of NetBackup Media & Primary servers on SuSE and RHEL.
    * Upgrade NetBackup environments (from and to NB version 10.x onwards).
* **Certificate Management**:
    * Independent certificate deployment, useful for initial setups or adding new primary servers.
* **Component Removal**:
    * Automated removal of NetBackup Client, Media, and Primary components.
* **EEB (Emergency Engineering Binary) Management**:
    * Deployment and management of EEBs with automatic marker creation for easy detection.
    * Supports installing multiple EEBs, upgrading EEBs, adjusting subsequent overlapping EEBs, and removing EEBs.
* **EEB Marker Creation Scripts**:
    * Automation includes scripts for creating EEB markers, simplifying detection of installed EEBs. Marker creation is supported for all platforms except AIX.
* **Package Staging**:
    * Option to cache NetBackup packages locally on target hosts for offline installations.
* **Global Security Settings**:
    * Apply global security settings to enhance secure communications.
* **Service Control**:
    * Playbooks to start, stop, and restart NetBackup services.
* **DirectIO Support**:
    * On RHEL, DirectIO is supported for Primary, Media, and Client. On Windows, DirectIO is supported for Client only.


## 🎯 Supported NetBackup Versions

These playbooks support the following NetBackup Primary, Media, and Client versions:
* `11.1.0.0`
* `11.0.0.1`
* `11.0.0.0`
* `10.5.0.1`
* `10.5.0.0`

## 🛠️ Playbooks

All playbooks are designed with Ansible's best practices in mind, offering:

* **Idempotency**: Ensures consistent results and allows for safe re-execution.
* **Task Logging**: Detailed logging for each task for better visibility and troubleshooting.
* **Co-located `ansible.cfg`**: Provides fine-grained control over Ansible behavior.
* **Extensibility**: Easy to integrate new custom roles.

The following table outlines the available playbooks and their functionalities, grouped for easier navigation:

---

### NetBackup Client Playbooks

#### Clients (Windows, SuSE, RHEL, Solaris, AIX, Linux P-series, Linux Z-series, Rocky Linux, and Oracle Linux)

| # | Playbook Name | Description & High-Level Workflow |
|---|---|---|
| 01 | [`playbook_install_client_linux.yml`](./playbook_install_client_linux.yml) | Performs fresh install or upgrade. Checks platform compatibility, installs missing dependent packages, runs defensive checks against Primary/Media roles, validates host state, performs installation/upgrade, deploys certificates if `nbu_cert_management` is true, performs connectivity validation, and installs provided EEBs. |
| 02 | [`playbook_upgrade_client_linux.yml`](./playbook_upgrade_client_linux.yml) | Part of the fresh install/upgrade workflow for Linux clients. |
| 03 | [`playbook_remove_client_linux.yml`](./playbook_remove_client_linux.yml) | Removes the specified NetBackup Client version. Runs defensive checks, verifies installed version, removes client footprint, and removes EEB markers. |

#### Windows Clients

| # | Playbook Name | Description & High-Level Workflow |
|---|---|---|
| 01 | [`playbook_install_client_windows.yml`](./playbook_install_client_windows.yml) | Performs fresh install or upgrade for Windows clients. |
| 02 | [`playbook_upgrade_client_windows.yml`](./playbook_upgrade_client_windows.yml) | Part of the fresh install/upgrade workflow for Windows clients. |
| 03 | [`playbook_remove_client_windows.yml`](./playbook_remove_client_windows.yml) | Removes the specified NetBackup Client version for Windows. |

---

### NetBackup Server Playbooks (Primary/Media)

#### Linux Servers (RHEL, SuSE, Oracle Linux)

| # | Playbook Name | Description & High-Level Workflow |
|---|---|---|
| 01 | [`playbook_install_media_linux.yml`](./playbook_install_media_linux.yml) | Performs fresh install or upgrade for Media servers. Checks platform compatibility, installs missing packages, performs space checks, runs defensive checks, validates host state, installs/upgrades, installs ITA Data Collector (if enabled), deploys certificates (if `nbu_cert_management` is true), performs connectivity validation, and installs provided EEBs. |
| 02 | [`playbook_upgrade_media_linux.yml`](./playbook_upgrade_media_linux.yml) | Part of the fresh install/upgrade workflow for Linux Media servers. |
| 03 | [`playbook_install_primary_linux.yml`](./playbook_install_primary_linux.yml) | Performs fresh install or upgrade for Primary servers. |
| 04 | [`playbook_upgrade_primary_linux.yml`](./playbook_upgrade_primary_linux.yml) | Part of the fresh install/upgrade workflow for Linux Primary servers. |
| 05 | [`playbook_remove_media_linux.yml`](./playbook_remove_media_linux.yml) | Removes the specified NetBackup Server version. Runs defensive checks, verifies installed version, removes footprint, removes ITA Data Collector if found, and removes EEB RPM markers. |
| 06 | [`playbook_remove_primary_linux.yml`](./playbook_remove_primary_linux.yml) | Removes the specified NetBackup Server version for Primary servers. |

---

### Common NetBackup Playbooks

#### Linux Platforms (RHEL, SuSE, Rocky Linux, Oracle Linux)

| # | Playbook Name | Description & High-Level Workflow |
|---|---|---|
| 01 | [`playbook_certificate_deployment_linux.yml`](./playbook_certificate_deployment_linux.yml) | Handles security configuration to establish connections between Primary, Clients, and Media. Can be used to add new primary servers or enroll external certificate authorities. Performs version checks and deploys certificates based on `nbu_cert_management` FTO. |
| 02 | [`playbook_stage_packages_locally_redhat.yml`](./playbook_stage_packages_locally_redhat.yml) | Downloads NetBackup RPM or DVD packages locally. Validates supported versions and downloads packages to local YUM repo cache. |
| 03 | [`playbook_start_services_linux.yml`](./playbook_start_services_linux.yml) | Starts all NetBackup services. |
| 04 | [`playbook_stop_services_linux.yml`](./playbook_stop_services_linux.yml) | Stops all NetBackup services. |
| 05 | [`playbook_restart_services_linux.yml`](./playbook_restart_services_linux.yml) | Restarts all NetBackup services. |

#### Windows Platforms

| # | Playbook Name | Description & High-Level Workflow |
|---|---|---|
| 01 | [`playbook_certificate_deployment_windows.yml`](./playbook_certificate_deployment_windows.yml) | Handles certificate deployment for Windows. |
| 02 | [`playbook_stage_packages_locally_windows.yml`](./playbook_stage_packages_locally_windows.yml) | Downloads NetBackup packages to local temp for Windows. |

#### Cross-Platform

| # | Playbook Name | Description & High-Level Workflow |
|---|---|---|
| 01 | [`playbook_configuration_global_settings.yml`](./playbook_configuration_global_settings.yml) | Updates Global Security Settings to enhance secure communications. |

---
## 🧩 Roles

These roles are integral to the playbooks and are called based on the required workflow. You typically do not need to modify their sequencing for the supported use cases.

<details>
<summary><b><u>Expand to find more details about roles</u></b></summary>

### Generic Roles (Immutable operations for validation or system checks)

| # | Role Name | Role Description |
|---|---|---|
| 01 | `generic/initiate_nbcheck` | Runs NBCheck before NetBackup installation or upgrade. Called only if `include_nbu_nbcheck` FTO is `true`. |
| 02 | `generic/is_nbu_version_supported` | Validates if the given proposed NetBackup version (`nbu_version`) is supported. |
| 03 | `generic/nbu_compatibility` | Performs preventive checks to validate NetBackup installation and compatibility with the Primary server version. |
| 04 | `generic/nbu_space_check` | Validates if the remote machine has sufficient space for NetBackup installation/upgrade. |
| 05 | `generic/nbu_verification` | Validates certificate-specific configurations. |
| 06 | `generic/os_compatibility` | Verifies OS compatibility for all supported NetBackup versions and installs missing system-dependent packages.

### Helper Roles

| # | Role Name | Role Description |
|---|---|---|
| 01 | `helper/nbu_role_status` | Performs a preventive check to validate whether the target host is not a Primary or Media server. |
| 02 | `helper/nbu_version_installed` | Reads the installed NetBackup version. |
| 03 | `helper/detect_partial_install` | Detects the partial installation state.

### NetBackup Roles (Performs system-level changes like installation, uninstallation, removal)

| # | Role Name | Role Description |
|---|---|---|
| 01 | `netbackup/common/nbu-get-certificate` | Checks the Primary Server's Certificate mode (NBCA/ECA) and performs certificate deployment for Client/Media installations accordingly. |
| 02 | `netbackup/common/stage-package-locally` | Staging playbook to download NetBackup packages into a local cache for use during install-time. |
| 03 | `netbackup/posix` <br> `netbackup/win32nt` | Contains static playbook specifications required for different workflows. |
| 04 | `netbackup/posix/nbu-client-install` <br> `netbackup/posix/nbu-server-install` <br> `netbackup/win32nt/nbu-client-install` | Installs/upgrades NetBackup Primary/Media/Client based on conditions like new install (no existing NetBackup or proposed version installed) or upgrade (older version installed). |
| 05 | `netbackup/posix/nbu-install-eeb`<br>`netbackup/win32nt/nbu-install-eeb` | Installs the list of EEBs provided in the initial configuration and creates a marker if `include_eeb_rpm_marker` FTO is `true`. |
| 06 | `netbackup/posix/nbu-remove` <br> `netbackup/win32nt/nbu-remove` | Removes NetBackup Primary/Media/Client only if the proposed version is found installed. |
| 07 | `netbackup/posix/nbu-stop-services` | Handles stopping NetBackup services if the proposed version is found installed. |
| 08 | `netbackup/posix/symlink-operations` | Deals with validation and creation of symbolic links on Linux. |
| 09 | `netbackup/posix/nbu-install-verification` | Performs validations to determine installation status (install/none/upgrade) based on existing and proposed NetBackup versions. |
| 10 | `netbackup/common/rest-api-integration` | Includes global security settings for configuring secure communications. |
| 11 | `netbackup/posix/nbu-start-services` <br> `netbackup/posix/nbu-stop-services` | Handles starting and stopping NetBackup services. |
| 12 | `netbackup/posix/pre-install-os-task` | Handles pre-installation OS tasks for Primary, including validating and creating specified local users/groups if missing.

</details>

---
## ⚙️ Variables

The user-centric variable files, `vars/linux.yml` and `vars/win32nt.yml`, must be updated to suit your environment. These files contain all the globally required inputs.

### Mandatory Variables

These variables are crucial for playbook execution.

| # | Input Variable | Description | Variable Type |
|---|---|---|---|
| 01 | `nbu_version` \* | Desired NetBackup Version (e.g., `x.x.x.x`). | `string` |
| 02 | `nbu_artifactory_repo_base_url` * | Base URL to the NetBackup yum repository. Can be a web server URL (e.g., `http://your.repo.com/`) or a local/mounted file-system path (e.g., `file:///path/to/your/repo/`). | `url` |
| 03 | `nbu_path_repo_base_pkg` \* | Path appended to the base URL for the NetBackup yum repository. | `url` |
| 04 | `nbu_path_repo_client_eeb_pkg` | Relative path of the EEB installer file. | `url` |
| 05 | `nbu_primary_server_ans` \* | Primary Server hostname. Required only for Media/Client. Default: `PRIMARY01`. | `string` |
| 06 | `nbu_cust_reg_file_name` \* | Usage insights customer registration key file for NetBackup Primary server installation/upgrade (`<= 10.2.0.1`). | `string` |

### Configurable Options

These variables offer flexible configuration for various scenarios.

| # | Input Variable | Description | Variable Type |
|---|---|---|---|
|  01 | `nbu_primary_certdetails` <br> (Mutually inclusive with `nbu_cert_management` FTO) | If the primary server uses only NBCA, the target host is configured using NBCA. Requires `hostname`, `nbu_server_fingerPrint`, and `nbu_server_authorization_token` in JSON format. | `JSON` |
| 02 | `nbu_eca_certdetails[Linux]` <br> (Mutually inclusive with `nbu_cert_management` FTO) | If the primary server uses ECA or mixed mode, the target host is configured with ECA. Requires `nbu_eca_cert_path`, `nbu_eca_private_key_path`, `nbu_eca_trust_store_path`. Optional `nbu_eca_key_passphrasefile` and `eca_crl` details. | `JSON` |
| 03 | `nbu_eca_certdetails[Windows]` <br> (Mutually inclusive with `nbu_cert_management` FTO) | Similar to Linux ECA configuration, supporting both file-based certificates and Windows Certificate Store. Requires `cert_store_type` (`windows_cert_store` or `windows_file_based`) and relevant paths/locations. | `JSON` |
| 04 | `nbu_eeb_ordered` | Specifies an ordered list of EEBs to be installed. Supports upgrading, handling overlapping EEBs, uninstalling, and providing special arguments. | `JSON` |
| 05 | `os_path_nbu_install` | Custom installation path for NetBackup. Default: `/usr/openv` for Linux, `C:\\Program Files\\Veritas` if nbu_version < 11.1 else `C:\\Program Files\\Cohesity NetBackup` for Windows. Recommended path ends with `openv` int Linux and `Veritas` or `Cohesity NetBackup` on Windows. | `string` |
| 06 | `nbu_directory_list_to_be_removed` | List of directories to be removed upon NetBackup uninstallation. | `list` |
| 07 | `os_rhel_system_packages` | Add custom OS dependent packages for RHEL systems. | `JSON` |
| 08 | `os_rhel_system_packages_symlink` | Add custom OS symlinks for RHEL systems. | `JSON` |
| 09 | `nbu_license_file_name_list` | NetBackup license file for Primary install/upgrade (for `>= 10.2.0.1`). | `list` |
| 10 | `nbu_webservices_group` | NetBackup webservices group. Default: `nbwebgrp`. | `string` |
| 11 | `nbu_webservices_user` | NetBackup webservices user. Default: `nbwebsvc`. | `string` |
| 12 | `nbu_services_group` | NetBackup services group. | `string` |
| 13 | `nbu_services_user` | NetBackup services user. | `string` |
| 14 | `nbu_database_user` | NetBackup database user. | `string` |
| 15 | `postgresql_pooler_odbc_port` | Optional PostgreSQL pooler ODBC port. Default: `13787`. | `string` |
| 16 | `security_properties_params` | Variables for global security settings (e.g., `certificateAutoDeployLevel`, `dteGlobalMode`). | `string` |
| 17 | `setPassphraseConstraintsRequest` | Variables for setting passphrase constraints (e.g., `minPassphraseLength`). | `string` |
| 18 | `drpkgpassphrase` | Variable required for disaster recovery passphrase. | `string` |
| 19 | `nbu_db_data_path` | Variable required to specify the PostgreSQL database user path. | `string` |
| 20 | `nbu_client_name_ans` | This variable is required for setting the FQDN(Fully Qualified Domain Name). | `string` |

### Feature Toggle Options (FTO)

These boolean variables enable or disable specific features.

| # | Input Variable | Description | Variable Type |
|---|---|---|---|
| 01 | `include_eeb_rpm_marker` | If `true`, an EEB marker is created during EEB installation. Default: `false`. | `bool` |
| 02 | `nb_include_java_jre_install` | If `true`, JAVA/JRE RPM packages are installed. Default: `false`. | `bool` |
| 03 | `nbu_cert_management[NBCA/ECA]` | If `true`, manages certificates. For NBCA, fetches host ID-based certificates from Primary. For ECA, uses external CA-signed certificates. Default: `true`. | `bool` |
| 04 | `do_perform_nbcheck_preinstall` | If `true`, runs NBCheck before installation/upgrade. Default: `true`. | `bool` |
| 05 | `install_pkgs_from_local_cache` | If `true`, packages are cached locally to avoid download at install-time. Default: `false`. | `bool` |
| 06 | `ignore_primary_connectivity_failures` | If `true`, ignores connectivity validation with Primary and continues execution. Default: `false`. | `bool` |
| 07 | `skip_primary_version_compatibility_check` | If `true`, skips Primary server version compatibility check. Default: `false`. | `bool` |
| 08 | `should_force_process_termination` | If `true`, forcefully terminates running processes after 3 graceful shutdown attempts. Default: `false`. | `bool` |
| 09 | `do_install_ita_dc` | If `true`, installs the ITA Data Collector optional package. Default: `true`. | `bool` |
| 10 | `skip_missing_catalog_backup_check` | If `true`, skips the check for a successful catalog backup in the last 24 hours. Default: `false`. | `bool` |
| 11 | `include_directio_install` | Controls whether the DirectIO (NetBackup DirectIO) package is installed for NetBackup Primary, Media, and Client servers. Options: `INCLUDE` (always install), `EXCLUDE` (never install), `MATCH` (follow the host's current configuration). Default: `MATCH`. | `string` |
|   | Note: DirectIO is only applicable from NetBackup version 11.1.0.0. |  |  |
---
## 🚀 Getting Started with NetBackup Ansible Playbooks

### Requirements/Prerequisites

Before running the playbooks, ensure the following:

1.  **Ansible Core**: Supports `ansible-core 2.15` onwards.
2.  **Ansible Automation Platform**: Must be configured and ready for use.
3.  **Non-interactive Connection**: Establish a non-interactive connection to all managed nodes/target hosts.
4.  **Artifact Repository Manager**: Configure an artifact repository manager (e.g., a yum repository) and upload all NetBackup RPMs with their respective repodata. This can be a web server accessible via URL, or a local/mounted file-system path.
    * **Client RPMs**: `<NB_Package_DIR>/NetBackup_<NB_VERSION>_CLIENTS2/NBClients/anb/Clients/usr/openv/netbackup/client/Linux/RedHat3.10.0`
    * **Primary/Media RPMs**: `<NB_Package_DIR>/NetBackup_<NB_VERSION>_LinuxR_x86_64/linuxR_x86/anb`
    * **Client Windows DVD Packages**: `<NB_Package_DIR>/NetBackup_<NB_VERSION>_Win\`
    * **ITA Data Collector (for Primary server)**: `<NB_Package_DIR>/NetBackup_<NB_VERSION>_LinuxR_x86_64/linuxR_x86/catalog/anb/ita_dc.tar.gz`
5.  **Ansible Inventory**: Ensure the Ansible inventory is pre-populated with your target hosts.


### Usage

Once all prerequisites are met, follow these steps to execute the playbooks:

#### Using Ansible CLI

Playbook execution requires certain mandatory variables.

1.  **Update Variables**:
    * Modify the template files `vars/linux.yml` (for Linux) or `vars/win32nt.yml` (for Windows) directly. These files are already included in all playbooks, so changes will be automatically picked up.
    * **Alternatively**, you can specify variables using the `--extra-vars` argument in JSON format, as supported by Ansible CLI.
2.  **Execute Playbook**: Run the `ansible-playbook` CLI command from the playbook's directory.

    * **Example (Linux with `vars/linux.yml` modified)**:
        ```bash
        [user@host ~]$ ansible-playbook playbook_install_client_linux.yml -l linux -vv
        ```
    * **Example (Windows with `vars/win32nt.yml` modified)**:
        ```bash
        [user@host ~]$ ansible-playbook playbook_install_client_windows.yml -l win -vv
        ```
    * **Example (Linux with `--extra-vars`)**:
        ```bash
        [user@host ~]$ ansible-playbook playbook_install_client_linux.yml -l linux -vv --extra-vars="nbu_version=10.3.0.0 os_path_nbu_install=/usr/openv"
        ```
    * **Example (Windows with `--extra-vars`)**:
        ```bash
        [user@host ~]$ ansible-playbook playbook_install_client_windows.yml -l win -vv --extra-vars="nbu_version=10.3.0.0"
        ```

#### From within the Ansible Automation Platform (e.g., AWX)

(At the time of this documentation, AWX is considered the web interface for managing the Ansible Automation Platform.)

1.  **AWX Configuration**: Ensure AWX is installed and initially configured:
    * Inventories are configured, and all target hosts are added with required credentials.
    * The project is created and synced using a supported Source Control Type.
2.  **Templates**:
    * AWX templates (also known as Ansible Tower Job Templates) are reusable blueprints for automating tasks.
    * Create a template and specify the project, inventory, and playbook to run.
    * If `vars/linux.yml` or `vars/win32nt.yml` is modified locally, the "Variables" field in the template can be left empty.
    * Otherwise, copy the entire content from the respective `vars` file and paste it into the "Variables" section in YAML format, updating values as needed for your environment.
3.  **Launch Template**: Launch the required template to begin playbook execution.

---
## 📜 License

### Disclaimer

The information in this publication is subject to change without notice. Cohesity, Inc. provides this manual "as is" and disclaims all warranties, including merchantability and fitness for a particular purpose. Cohesity, Inc. is not liable for errors or consequential damages related to the use of this manual. 
The software is provided under a license agreement and must be used in accordance with its terms.

### Legal Notice

Last updated: 2025-10-25
Copyright © 2025 Cohesity, Inc. All rights reserved.
Cohesity, the Cohesity Logo, and other Cohesity Marks are trademarks of Cohesity, Inc. or its affiliates in the US and/or internationally. Other names may be trademarks of their respective owners.
This product may contain third-party software under open source or free software licenses. The license agreement does not alter your rights or obligations under these licenses. The product and documentation are distributed under licenses restricting use, copying, distribution, and decompilation/reverse engineering. No part of this document may be reproduced without prior written authorization from Cohesity, Inc.
THE DOCUMENTATION IS PROVIDED "AS IS" AND ALL EXPRESS OR IMPLIED CONDITIONS, REPRESENTATIONS AND WARRANTIES, INCLUDING ANY IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT, ARE DISCLAIMED, EXCEPT TO THE EXTENT THAT SUCH DISCLAIMERS ARE HELD TO BE LEGALLY INVALID. COHESITY, INC. SHALL NOT BE LIABLE FOR INCIDENTAL OR CONSEQUENTIAL DAMAGES IN CONNECTION WITH THE FURNISHING, PERFORMANCE, OR USE OF THIS DOCUMENTATION. THE INFORMATION CONTAINED IN THIS DOCUMENTATION IS SUBJECT TO CHANGE WITHOUT NOTICE.
The licensed Software and Documentation are deemed to be commercial computer software as defined in FAR 12.212 and subject to restricted rights as defined in FAR Section 52.227-19 "Commercial Computer Software - Restricted Rights" and DFARS 227.7202, et seq. "Commercial Computer Software and Commercial Computer Software Documentation," as applicable, and any successor regulations, whether delivered by Cohesity as on premises or hosted services. Any use, modification, reproduction release, performance, display or disclosure of the Licensed Software and Documentation by the U.S. Government shall be solely in accordance with the terms of this Agreement.

Cohesity, Inc.
2625 Augustine Drive
Santa Clara, CA 95054

### Third-Party Legal Notices

Cohesity offerings may include third-party materials that are subject to a separate license. A list of those materials is accessible in the product user interface, in a Cohesity-hosted support portal made available to Cohesity Support customers, or included in the ReadMe file or Documentation for the applicable offering.
