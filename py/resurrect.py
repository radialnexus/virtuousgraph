import os
import sys
import shutil
import argparse
import yaml

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
        print(f"\033[{color}m{formatted_text.format(**kwargs)}\033[0m")

def restore_directory_structure(domain_name):
    Esse.printf("____________restore_directory_structure____________\n", GREEN)
    """
    Restore the necessary directory structure for a previously deprecated domain.
    """
    bak_path = os.path.join('..', 'bak', domain_name)
    domain_path = os.path.join('..', 'domain', domain_name)

    if os.path.exists(bak_path):
        shutil.move(bak_path, domain_path)
        print(f"Moved {domain_name} directory to ../domain/{domain_name}")
    else:
        print(f"No backup found for domain '{domain_name}' in ../bak.")

def copy_restored_files(domain_name):
    Esse.printf("____________copy_restored_files____________\n", GREEN)
    """
    Copy the restored JSON and PNG files to their respective Vue directories.
    """
    # Copy PNG
    png_path = os.path.join('..', 'domain', domain_name, 'png', f"{domain_name}.png")
    dest_png_path = os.path.join('..', 'vue', 'src', 'assets', f"{domain_name}.png")
    if os.path.exists(png_path):
        shutil.copy(png_path, dest_png_path)
        print(f"Copied {domain_name}.png to assets/{domain_name}.png")

    # Copy JSON
    json_path = os.path.join('..', 'domain', domain_name, 'json', f"{domain_name}.json")
    dest_json_path = os.path.join('..', 'vue', 'public', 'domain', f"{domain_name}.json")
    if os.path.exists(json_path):
        shutil.copy(json_path, dest_json_path)
        print(f"Copied {domain_name}.json to public/domain/{domain_name}.json")

def modify_vue_files(domain_name, domain_yaml):
    Esse.printf("____________modify_vue_files____________\n", GREEN)
    """
    Modify Vue files to add the restored domain.
    """
    vue_path = os.path.join('..', 'vue', 'src')
    main_js_path = os.path.join(vue_path, 'main.js')
    landing_page_path = os.path.join(vue_path, 'views', 'LandingPage.vue')
    domain_graph_path = os.path.join(vue_path, 'views', f'{domain_name.capitalize()}Graph.vue')

    # Update main.js
    with open(main_js_path, 'r') as file:
        main_js = file.read()

    component_insert = f"\n// Import {domain_name.capitalize()}Graph.vue component\nimport {domain_name.capitalize()}Graph from './views/{domain_name.capitalize()}Graph.vue';"
    route_insert = f"\n    {{ path: '/{domain_name}', component: {domain_name.capitalize()}Graph }},"

    if component_insert not in main_js:
        main_js = main_js.replace('// BEGIN insert component', f'// BEGIN insert component{component_insert}')
    if route_insert not in main_js:
        main_js = main_js.replace('// BEGIN insert route', f'// BEGIN insert route{route_insert}')

    with open(main_js_path, 'w') as file:
        file.write(main_js)
    
    print(f"Modified main.js with {domain_name.capitalize()}Graph component and route")

    # Update LandingPage.vue
    with open(landing_page_path, 'r') as file:
        landing_page = file.read()

    title = domain_yaml.get('title', f'{domain_name.capitalize()}')
    headline = domain_yaml.get('headline', f'{domain_name.capitalize()}')
    description = domain_yaml.get('description', f'{domain_name.capitalize()}')

    landing_page_insert = f"""
        {{
          title: '{title}',
          headline: '{headline}',
          description: '{description}.',
          imageSrc: require('@/assets/{domain_name}.png'),
          route: '/{domain_name}'
        }},
    """

    if landing_page_insert not in landing_page:
        landing_page = landing_page.replace('/* BEGIN insert domain */', f'/* BEGIN insert domain */{landing_page_insert}')

    with open(landing_page_path, 'w') as file:
        file.write(landing_page)
    
    print(f"Modified LandingPage.vue with new domain {domain_name}")

    # Copy Graph.vue file from backup
    src_graph_path = os.path.join('..', 'domain', domain_name, 'vue', f'{domain_name.capitalize()}Graph.vue')
    if os.path.exists(src_graph_path):
        shutil.copy(src_graph_path, domain_graph_path)
        print(f"Copied {domain_name.capitalize()}Graph.vue from backup")
    else:
        print(f"NOT Copied {domain_name.capitalize()}Graph.vue from backup")

def load_domain_yaml(domain_name):
    Esse.printf("____________load_domain_yaml____________\n", GREEN)
    """
    Load the Model.yaml file with any prefix in the name from the backup yaml directory.
    """
    yaml_dir = os.path.join('..', 'domain', domain_name, 'yaml')
    model_file = None
    for filename in os.listdir(yaml_dir):
        if filename.endswith("Model.yaml"):
            model_file = os.path.join(yaml_dir, filename)
            break

    if model_file:
        with open(model_file, 'r') as file:
            return yaml.safe_load(file)
    else:
        print(f"No Model.yaml file found for {domain_name}.")
        return {}

def main(domain_name):
    Esse.printf("____________Main____________\n", GREEN)
    Esse.printf("Domain: {domain_name}\n", BLUE, domain_name=domain_name)

    # Step 1: Restore directory structure
    restore_directory_structure(domain_name)

    # Step 2: Copy restored JSON and PNG files to Vue directories
    copy_restored_files(domain_name)

    # Step 3: Modify Vue files with values from Model.yaml in backup
    domain_yaml = load_domain_yaml(domain_name)
    modify_vue_files(domain_name, domain_yaml)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore a previously deprecated domain.")
    parser.add_argument('domain_name', type=str, help='The name of the domain to restore.')
    
    args = parser.parse_args()
    main(args.domain_name)

# Run the script like so:
# conda activate dev
# python3 resurrect.py tube
