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
        # TODO: Conditional?
        print(f"\033[{color}m{formatted_text.format(**kwargs)}\033[0m")

def create_directory_structure(domain_name):
    Esse.printf("____________create_directory_structure____________\n", GREEN)
    """
    Create the necessary directory structure for a new domain.
    """
    base_path = os.path.join('..', 'domain', domain_name)
    directories = [
        'bak',     
        'csv/data',
        'json',
        'png',
        'py',     
        'sor',     
        'xls',              
        'yaml'
    ]
    
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")
    
def copy_starter_files(domain_name):
    Esse.printf("____________copy_starter_files____________\n", GREEN)
    """
    Copy starter files from the ~/sor/ directory into the new domain directories.
    """
    # Copy Mapping.csv to the csv/ directory
    shutil.copy(os.path.join('..', 'sor', 'Mapping.csv'), os.path.join('..', 'domain', domain_name, 'csv', 'Mapping.csv'))
    print(f"Copied Mapping.csv to {os.path.join('..', 'domain', domain_name, 'csv')}")

    # Copy domain.csv to the csv/data directory
    shutil.copy(os.path.join('..', 'sor', 'domain.csv'), os.path.join('..', 'domain', domain_name, 'csv/data', f'{domain_name}.csv'))
    print(f"Copied domain.csv to {os.path.join('..', 'domain', domain_name, 'csv/data', '{domain_name}.csv')}")

    # Copy Model.yaml to the yaml/ directory
    shutil.copy(os.path.join('..', 'sor', 'Model.yaml'), os.path.join('..', 'domain', domain_name, 'yaml', 'Model.yaml'))
    print(f"Copied Model.yaml to {os.path.join('..', 'domain', domain_name, 'yaml')}")

    # Copy Modality.yaml to the yaml/ directory
    shutil.copy(os.path.join('..', 'sor', 'Modality.yaml'), os.path.join('..', 'domain', domain_name, 'yaml', 'Modality.yaml'))
    print(f"Copied Modality.yaml to {os.path.join('..', 'domain', domain_name, 'yaml')}")

def modify_vue_files(domain_name, domain_yaml):
    Esse.printf("____________modify_vue_files____________\n", GREEN)
    """
    Modify Vue files to add the new domain.
    """
    # Paths to important Vue files
    vue_path = os.path.join('..', 'vue', 'src')
    main_js_path = os.path.join(vue_path, 'main.js')
    landing_page_path = os.path.join(vue_path, 'views', 'LandingPage.vue')
    domain_graph_path = os.path.join(vue_path, 'views', f'{domain_name.capitalize()}Graph.vue')
    
    # Read and modify ~/vue/src/main.js
    with open(main_js_path, 'r') as file:
        main_js = file.read()
    
    # Insert component and route into main.js
    component_insert = f"\n// Import {domain_name.capitalize()}Graph.vue component\nimport {domain_name.capitalize()}Graph from './views/{domain_name.capitalize()}Graph.vue';"
    route_insert = f"\n    {{ path: '/{domain_name}', component: {domain_name.capitalize()}Graph }},"

    if component_insert not in main_js:
        main_js = main_js.replace('// BEGIN insert component', f'// BEGIN insert component{component_insert}')
    if route_insert not in main_js:
        main_js = main_js.replace('// BEGIN insert route', f'// BEGIN insert route{route_insert}')
    
    # Write back to main.js
    with open(main_js_path, 'w') as file:
        file.write(main_js)
    
    print(f"Modified main.js with {domain_name.capitalize()}Graph component and route")

    # Modify ~/vue/src/views/LandingPage.vue
    with open(landing_page_path, 'r') as file:
        landing_page = file.read()
    
    # Extract values from the domain yaml
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
    
    # Write back to LandingPage.vue
    with open(landing_page_path, 'w') as file:
        file.write(landing_page)

    print(f"Modified LandingPage.vue with new domain {domain_name}")

    # Copy DomainGraph.vue template and modify it
    shutil.copy(os.path.join('..', 'sor', 'DomainGraph.vue'), domain_graph_path)
    
    with open(domain_graph_path, 'r') as file:
        domain_graph_vue = file.read()

    # Modify template, name, and fetch for the new domain
    domain_graph_vue = domain_graph_vue.replace('domain-graph', f'{domain_name}-graph')
    domain_graph_vue = domain_graph_vue.replace('DomainGraph', f'{domain_name.capitalize()}Graph')
    domain_graph_vue = domain_graph_vue.replace("fetch('domain/domain.json')", f"fetch('domain/{domain_name}.json')")

    # Write back to <Domain>Graph.vue
    with open(domain_graph_path, 'w') as file:
        file.write(domain_graph_vue)
    
    print(f"Copied and modified {domain_name.capitalize()}Graph.vue")

def copy_domain_image(domain_name):
    """
    Copy the domain image from ~/sor/ to the Vue assets directory.
    Checks if a specific PNG for the domain exists; otherwise, uses domain.png.
    """
    src_dir = os.path.join('..', 'sor')
    dest_dir = os.path.join('..', 'vue', 'src', 'assets')
    
    # Define paths for specific domain image and fallback image
    specific_image_path = os.path.join(src_dir, f"{domain_name}.png")
    default_image_path = os.path.join(src_dir, "domain.png")
    dest_image_path = os.path.join(dest_dir, f"{domain_name}.png")
    
    # Check if specific domain image exists, otherwise use default
    if os.path.exists(specific_image_path):
        shutil.copy(specific_image_path, dest_image_path)
        print(f"Copied {domain_name}.png to assets/{domain_name}.png")
    else:
        shutil.copy(default_image_path, dest_image_path)
        print(f"Copied domain.png to assets/{domain_name}.png (default image used)")


def copy_domain_json(domain_name):
    Esse.printf("____________copy_domain_json____________\n", GREEN)
    """
    Copy the domain json from ~/sor/ to the Vue public/domain directory.
    """
    shutil.copy(os.path.join('..', 'sor', 'domain.json'), os.path.join('..', 'vue', 'public', 'domain', f'{domain_name}.json'))
    print(f"Copied domain.json to public/domain/{domain_name}.json")

def load_domain_yaml(domain_name):
    Esse.printf("____________load_domain_yaml____________\n", GREEN)
    """
    Load the domain.yaml file if it exists.
    """
    # yaml_path = os.path.join('..', 'sor', f'{domain_name}.yaml')
    yaml_path = os.path.join('..', 'domain', domain_name, 'yaml', 'Model.yaml')
    
    if os.path.exists(yaml_path):
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)
    else:
        print(f"No yaml file found for {domain_name}. Proceeding without it.")
        return {}

def main(domain_name):
    Esse.printf("____________Main____________\n", GREEN)
    Esse.printf("Domain: {domain_name}\n", BLUE, domain_name=domain_name)
    """
    Main function to instantiate a new domain's directory structure and update files for Force graph visualization.
    """

    # Step 1: Create directory structure
    create_directory_structure(domain_name)
    
    # Step 2: Copy starter files (Mapping.csv, Model.yaml)
    copy_starter_files(domain_name)

    # Step 3: Modify Vue files
    domain_yaml = load_domain_yaml(domain_name)
    modify_vue_files(domain_name, domain_yaml)
    
    # These will need to be modified by user after manifestation (for json) and png of choice
    # Step 4: Copy domain.png to assets
    copy_domain_image(domain_name)
    
    # Step 5: Copy domain.json to public
    copy_domain_json(domain_name)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instantiate a new domain.")
    parser.add_argument('domain_name', type=str, help='The name of the domain to instantiate.')
    
    args = parser.parse_args()
    main(args.domain_name)

# conda activate dev
# python3 instantiate.py tube
# python3 instantiate.py manifest
