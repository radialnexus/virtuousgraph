import os
import sys
import shutil
import time
import argparse

# Colors for printing
RED = "31;1"
GREEN = "32;1"
YELLOW = "33;1"
BLUE = "34;1"

# Meta class for all classes
class Esse:  
    # Print Formatted String with Keywords
    @staticmethod
    def printf(formatted_text, color, **kwargs):
        # TODO: Conditional?
        print(f"\033[{color}m{formatted_text.format(**kwargs)}\033[0m")

def backup_directory(domain_name):
    Esse.printf("____________backup_directory____________\n", GREEN)
    # Define paths
    src_path = f"../domain/{domain_name}"
    bak_path = f"../bak/"
    backup_path = f"../bak/{domain_name}"

    Esse.printf("src_path: {src_path} backup_path: {backup_path}\n", BLUE, src_path=src_path, backup_path=backup_path)

    # Check if the source path exists
    if os.path.exists(src_path):
        # Check if the backup path already exists
        if os.path.exists(backup_path):
            user_choice = input(f"The backup directory '{backup_path}' already exists. "
                                "Do you want to overwrite it (o), rename the backup (r), or cancel (c)? ").strip().lower()
            if user_choice == 'o':
                # Overwrite existing backup by removing it and then moving
                shutil.rmtree(backup_path)
                shutil.move(src_path, bak_path)
                print(f"Overwritten existing backup for '{domain_name}' at '{backup_path}'.")
            elif user_choice == 'r':
                # Ask for a new name and move to the renamed path
                new_bak_path = f"../bak/{domain_name}_{int(time.time())}"  # Append timestamp to ensure uniqueness
                shutil.move(src_path, new_bak_path)
                print(f"Backup renamed to '{new_bak_path}'.")
            else:
                print("Operation canceled.")
                sys.exit()  # Exit the script entirely
        else:
            # If backup path doesn't exist, move without issue
            shutil.move(src_path, bak_path)
            print(f"Moved '{domain_name}' to '{backup_path}'.")
    else:
        print(f"The source directory '{src_path}' does not exist.") 

    # Create backup directory and subdirectories
    os.makedirs(backup_path, exist_ok=True)
    os.makedirs(os.path.join(backup_path, "png"), exist_ok=True)
    os.makedirs(os.path.join(backup_path, "vue"), exist_ok=True)
    os.makedirs(os.path.join(backup_path, "js"), exist_ok=True)


    # Backup added assets
    capitalized_domain_name = domain_name.capitalize()
    assets_to_backup = [
        (f"../vue/src/assets/{domain_name}.png", os.path.join(backup_path, "png")),
        (f"../vue/src/views/{capitalized_domain_name}Graph.vue", os.path.join(backup_path, "vue"))
    ]

    for asset_path, dest_dir in assets_to_backup:
        if os.path.exists(asset_path):
            shutil.move(asset_path, os.path.join(dest_dir, os.path.basename(asset_path)))

    # Backup modified files
    modified_files = {
        "../vue/src/main.js": os.path.join(backup_path, "js", "main.js"),
        "../vue/src/views/LandingPage.vue": os.path.join(backup_path, "vue", "LandingPage.vue")
    }
    
    for file_path, backup_file_path in modified_files.items():
        if os.path.exists(file_path):
            shutil.copy2(file_path, backup_file_path)

def revert_modifications(domain_name):
    Esse.printf("____________revert_modifications____________\n", GREEN)
    main_js_path = "../vue/src/main.js"
    landing_page_path = "../vue/src/views/LandingPage.vue"
    
    # Revert main.js by removing specific domain component and route
    with open(main_js_path, "r") as file:
        lines = file.readlines()

    # Flags for tracking removal states
    inside_insert_component = inside_insert_route = False
    component_comment_line = f"// Import {domain_name.capitalize()}Graph.vue component"
    domain_component_line = f"import {domain_name.capitalize()}Graph from './views/{domain_name.capitalize()}Graph.vue';"
    domain_route_line = f"{{ path: '/{domain_name}', component: {domain_name.capitalize()}Graph }},"

    with open(main_js_path, "w") as file:
        for line in lines:
            # Process component lines
            if "// BEGIN insert component" in line:
                inside_insert_component = True
                file.write(line)
            elif "// END insert component" in line:
                inside_insert_component = False
                file.write(line)
            elif inside_insert_component and (component_comment_line in line or domain_component_line in line):
                continue  # Skip both the component comment and import line for the domain
            elif not inside_insert_component:
                file.write(line)

    # Revert main.js by removing specific domain component and route
    with open(main_js_path, "r") as file:
        lines = file.readlines()

    with open(main_js_path, "w") as file:
        for line in lines:
            # Process route lines
            if "// BEGIN insert route" in line:
                inside_insert_route = True
                file.write(line)
            elif "// END insert route" in line:
                inside_insert_route = False
                file.write(line)
            elif inside_insert_route and domain_route_line in line:
                continue  # Skip this specific route line for the domain
            elif not inside_insert_route:
                file.write(line)

    # Revert LandingPage.vue by removing specific domain entry
    with open(landing_page_path, "r") as file:
        lines = file.readlines()

    domain_entry_start = f"{{\n          title: '{domain_name.capitalize()}',"
    with open(landing_page_path, "w") as file:
        inside_insert_domain = False
        skip_domain_block = False
        for line in lines:
            if "/* BEGIN insert domain */" in line:
                Esse.printf("Inside", RED)
                inside_insert_domain = True
                Esse.printf("{line}", GREEN, line=line)
                file.write(line)
            elif "/* END insert domain */" in line:
                Esse.printf("Outside", BLUE)
                inside_insert_domain = False
                Esse.printf("{line}", GREEN, line=line)
                file.write(line)
            # elif inside_insert_domain and domain_entry_start in line:
            elif inside_insert_domain:
                Esse.printf("{line}", RED, line=line)
                skip_domain_block = True
            # elif skip_domain_block and line.strip() == "},":
            #     Esse.printf("NO SKIP", BLUE)
            #     skip_domain_block = False
            # elif not inside_insert_domain or not skip_domain_block:
            elif not inside_insert_domain:
                file.write(line)

def deprecate_domain(domain_name):
    Esse.printf("____________deprecate_domain____________\n", GREEN)
    # Backup and move files
    backup_directory(domain_name)

    # Revert modifications in Vue files
    revert_modifications(domain_name)

def main(domain_name):
    Esse.printf("____________Main____________\n", GREEN)
    Esse.printf("Domain: {domain_name}\n", BLUE, domain_name=domain_name)

    deprecate_domain(args.domain_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deprecate a domain from the project.")
    parser.add_argument("domain_name", type=str, help="The name of the domain to deprecate.")
    args = parser.parse_args()
    main(args.domain_name)

# Deprecate the last instantiation, reverting application to original state.
# python3 deprecate.py northwind
# python3 deprecate.py tube
# python3 deprecate.py manifest

