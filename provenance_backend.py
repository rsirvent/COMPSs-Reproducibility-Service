"""
RS provenance flag logic Module

This module gets used in case the user triggers the provenance flag. It does the necessary
steps to generate the provenence for COMPSs Runtime


Functions:
    - update_yaml(crate_path: str)


    - provenance_info_collector() -> bool
      Collects the provenance information from the user
"""
import os
import time

from rocrate.rocrate import ROCrate
from ruamel.yaml import YAML
from utils import get_instument, get_yes_or_no, get_name_and_description, get_ro_crate_info

def update_yaml(crate_path: str):
    """
    Update the 'ro-crate-info.yaml' file with workflow metadata.

    Args:
        crate_path (str): Path to the root directory of the RO-Crate.

    Raises:
        FileNotFoundError: If the specified files or directories do not exist.

    Notes:
        This function updates the 'ro-crate-info.yaml' file with metadata such as sources,
        main file, name, and description retrieved from the RO-Crate.
    """
    crate = ROCrate(crate_path)
    instrument = get_instument(crate)
    sources_main_file = os.path.join(crate_path, instrument)
    sources = os.path.join(crate_path, "application_sources")
    name, description = get_name_and_description(crate_path)
    # Create a YAML instance
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml_file_path = './ro-crate-info.yaml'
    # Read the YAML content from the file
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

    # Update the name and description fields
     # Update the fields in the loaded YAML content
    data['COMPSs Workflow Information']['sources'] = sources
    data['COMPSs Workflow Information']['sources_main_file'] = sources_main_file
    data['COMPSs Workflow Information']['name'] = name
    data['COMPSs Workflow Information']['description'] = description

    # Write the updated dictionary back to the YAML file
    with open(yaml_file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

    print("YAML file updated successfully.")

def provenance_info_collector() -> bool:
    """
    Collect provenance information for the workflow based on user input.

    Returns:
        bool: True if provenance collection is enabled; False otherwise.

    Notes:
        This function prompts the user to confirm if they want to collect provenance information.
        If confirmed, it checks for the existence of 'ro-crate-info.yaml' file and prompts the user
        to ensure it is filled correctly. If not found or verified, it invokes 'get_ro_crate_info'
        to generate the file. It returns True if provenance collection is enabled, False otherwise.
    """
    provenance_flag = get_yes_or_no("Do you want to see the provenance of the workflow?")
    print(provenance_flag)
    if provenance_flag:
        current_dir = os.getcwd()
        files = os.listdir(current_dir)
        already_exists = "ro-crate-info.yaml" in files
        time.sleep(1)
        if not already_exists :
            get_ro_crate_info()
            print("Please fill the ro-crate-info.yaml file, generated inside the current working directory.")
            time.sleep(1)
            check = False
            while not check:
                time.sleep(1)
                check = get_yes_or_no("Have you filled the ro-crate-info.yaml file for provenance generation?")
        else:
            print("ro-crate-info.yaml file already exists in the current working directory.")
            check = get_yes_or_no("Please check if the already existing ro-crate-info.yaml file is correctly filled for provenance generation")

            if not check:
                get_ro_crate_info()
                time.sleep(1)
                print("Please fill the new ro-crate-info.yaml file, generated inside the current working directory.")
                check = False
                while not check:
                    time.sleep(1)
                    check = get_yes_or_no("Have you filled the ro-crate-info.yaml file for provenance generation?")

        print("Considering the filled information for provenance generation.")

    return provenance_flag
