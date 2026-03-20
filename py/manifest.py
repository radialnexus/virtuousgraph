"""
Manifests the Graph from various inputs to various outputs using the Graph itself.

python3 manifest.py trees Graph Cypher Exceptional_Trees_On_Oahu

Parameters: Here's an explanation of the parameters above

    trees:      the top-level directory containing the Domain of Discourse
    Graph:      the desired Manifestation
    Cypher:     the required Transformation
    Source:     the current Source

Structure:  Here's the directory structure the example currently assumes

    domains/
        trees/
            02_Mapping.csv
            csv/
                data/
                info/
            json/
            py/

Process:  Here's an overview of the current implementation.

The overall goal of the script is to take a mapping of a graph in simple format (currently a 
spreadsheet, soon a graph itself) and manifest that mapping into a Graph.  It's envisaged that
the script will be used to mapping many different domains.  A number of assumptions have been
made about the directory structure as a result.  Under domains, will be the current Domain of
Interest.  There will be a subdirectory within that will correspond to the first parameter.  
From there, the script assumes the Mapping will be at the top of that subdirectory and will be
of the form *Mapping.csv (use a versioning system that starts with 2 digits and an underscore).
From there, the script assumes the actual data files will be in csv and are in a subdirectory
so named within a data subdirectory therein.  

The key differentiating point for the script is its integration of the Graph into the Code and
its view of Code as a Graph.  Inheritance is used, with Classes corresponding to parameters so 
that the specific Transformer can be specified and executed against.

Execution:

First, install a Desktop version of Neo4j.  Then add to your shell profile:

    export NEO4J_USERNAME=neo4j
    export NEO4J_PASSWORD=<pwd>
    export NEO4J_BOLT_URL="bolt://$NEO4J_USERNAME:$NEO4J_PASSWORD@localhost:7687"
    export NEO4J_BASE_URL="bolt:/localhost:7687"

From a subdirectory parallel to domains, run the method as follows:

    python3 manifest.py trees Graph Cypher Exceptional_Trees_On_Oahu

Then in the py subdirectory there will be 

    <domain>.py 

script generated.  Run that script:

    python3 <domain>.py

to load the graph.  Share and Enjoy.

Copyright(c), 2023, Michael Bauer.  All Rights Reserved.


"""
import os
import sys
import glob
import argparse
import chardet
import fnmatch
import pprint
import re
import pandas as pd
import numpy as np
import math
import json
import yaml
import random

#import unicodedata
from unidecode import unidecode

# Root paths and set types for configuration and mapping files
ROOT_PATH = "../"
FORCE_PATH = "../vue/public/"
DOMAIN_PITH = "domain"
MANIFEST_TYPE = "yaml"
MODEL_TYPE = "yaml"
MAPPING_TYPE = "csv"

# Configuration piths for software and the domain
MANIFEST_PITH = "manifest"
MODEL_PITH = "Model"
MAPPING_PITH = "Mapping"
MODALITY_PITH = "Modality"

EXPLICIT = "explicit"
IMPLICIT = "implicit"

# Placeholder constants for software mapping using csv file and a single transformation method
SOURCE_COLUMN = "Column"
GENERATION_METHOD = "generate"

# Constants for file analysis
SAMPLE_INPUT_SIZE = 10000
DEFAULT_ENCODING = 'UTF-8'

# Default Colors for Edges
EDGE_COLOR = 'CCCCCC'
EDGE_STRENGTH = '5'

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

    # Instantiate any Class dynamically
    @staticmethod
    def instantiate(class_type, *args, **kwargs):
        # Esse.printf("____________Esse: Instantiate____________\n", GREEN)             
        if class_type not in globals():
            raise ValueError(f"Invalid Class Type: {class_type}")
        instance = globals()[class_type](*args, **kwargs)
        return instance

    # Extricate method from instance by name     
    @staticmethod
    def extricate(instance, method_name):
        #Esse.printf("____________Esse: Extricate____________\n", GREEN)             
        #Esse.printf("Method: {method_name}", YELLOW, method_name=method_name)
        method = getattr(instance, method_name, None)
        return method

    # Get a class by name
    def get_class(self, class_name):
        if class_name not in globals():
            raise ValueError(f"Invalid Class Name: {class_name}")
        return globals()[class_name]

    # Get a constant from a class 
    def get_constant(self, class_ref, constant_name):
        if not hasattr(class_ref, constant_name):
            raise AttributeError(f"Constant '{constant_name}' not found in class '{class_ref.__name__}'")    
        return getattr(class_ref, constant_name)
        
    # General "Print" statement. 
    def inspect(self):
        esse = type(self).__name__
        self.printf("{esse}:", RED, esse=esse)
        attributes = {attr: getattr(self, attr) for attr in dir(self) if not attr.startswith("__") and not callable(getattr(self, attr))}
        [print(f"{key}:", value) for key, value in attributes.items()]
        print("\n")

    # Get Variable name from a Value
    def get_variable_name(self, name, qualifier=None):
        name = self.knas(name)
        variable = name.lower()
        return variable
    
    # Get Method name from a Value
    def get_method_name(self, name, qualifier=None):
        name = self.knas(name)
        variable = name.lower()
        return variable

    # Know Null As Empty String
    def knas(self, value):
        knas = value
        if isinstance(value, (int,float)):
            if math.isnan(value):
                knas = ""
            else:
                knas = value
        if knas is None:
            knas = ""
        return knas
    
    # Know Value is Null
    @staticmethod
    def kisn(value):
        Esse.printf("____________kisn [{value}]____________\n", YELLOW, value=value)
        kisn = False
        if value == '' or value is None or pd.isna(value):
            kisn = True
        Esse.printf("____________kisn [{kisn}]____________\n", YELLOW, kisn=kisn)
        return kisn
    
    # Print any Type dynamically
    @staticmethod
    def print_type(esse):
        esse_type = type(esse)
        esse_name = str(esse_type)[8:-2]
        Esse.printf("Esse: {esse_name}", RED, esse_name=esse_name)

    @staticmethod
    def uniexcode(source_str):
        # Using unicodedata
        # nfkd_form = unicodedata.normalize('NFKD', source_str)
        # normalized_form = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
        # Using unidecode
        normalized_form = source_str
        normalized_form = unidecode(source_str)
        normalized_form = normalized_form.replace('`', '')
        #normalized_form = normalized_form.replace("'", "")        
        return normalized_form

# Meta Python convenience class
class Struct(Esse):
    def __init__(self):
        pass
    
# Dictionary convenience class
class Dict(Struct):

    # Get first key from dictionary
    @staticmethod
    def key(dictionary):
        return next(iter(dictionary.keys()))        
        
    # Get first value from dictionary
    @staticmethod
    def value(dictionary):
        return next(iter(dictionary.values()))     
        
    # Print Formatted Dictionary
    @staticmethod
    def printf(dictionary):
        Esse.printf("\nDictionary:", RED)
        # print(json.dumps(dictionary, indent=4))
        formatted_output = '\n'.join(f"{key}: {value}" for key, value in dictionary.items())
        print(formatted_output)        
        # Esse.printf("\ndone\n", RED)

# Data Frame convenience class
class DF(Struct):
    # Split Data Frame into a Dictionary of Data Frames based on a column, retaining sort order
    @staticmethod
    def split(df, column):
        df_dict = {}
        if df is not None:
            grouped = df.groupby(column, sort=False)
            df_dict = { column: group for column, group in grouped}
        return df_dict

    @staticmethod
    def unique(df, column):
        unique_values = []
        unique_values = df[column].unique().tolist()        
        return unique_values

    # Extract Series from Data Frame by Column Value
    @staticmethod
    def extract_series(node_name, node_df, column, value):
        # Esse.printf("____________extract_series____________\n", YELLOW)
        # DF.printf(node_name, node_df)
        # filtered_df = node_df[node_df[column] == value]
        # DF.printf("Filtered", filtered_df)
        series = node_df[node_df[column] == value].iloc[0]
        redux_df = node_df[node_df[column] != value]
        return series, redux_df

    # Print a Data Frame
    @staticmethod
    def printf(name, df, columns=None):
        column_names = ', '.join(columns) if columns is not None else "All columns"        
        Esse.printf("{name} Data Frame [{column_names}]", BLUE, name=name, column_names=column_names)        
        if columns is not None:
            column_keys = columns[0]
            print(df[column_keys])
        else:
            print(df)
        print("\n")

    # Print a Dictionary of Data Frames
    @staticmethod
    def print_dfs(dataframes):
        formatted_output = '\n\n'.join(f"{key}: {value}" for key, value in dataframes.items())
        print(formatted_output)

# List convenience class
class List(Struct):
   # Print a Data Frame prefaced with name
   @staticmethod
   def printf(name, alist, code=RED):
       Esse.printf("{name}: {alist}", code, name=name, alist=alist)        
       
# Series convenience class
class Series(Struct):
   # Print a Data Frame prefaced with name
   @staticmethod
   def printf(name, series, code=RED):
       Esse.printf("{name} Series:", code, name=name)        
       print(series)
       print("\n")
    
# File interrogation and extraction
class File(Esse):
    # Initialize the File Attributes (path, base, pith)
    def __init__(self, path):
        self.path = path
        try:
            self.base = os.path.basename(path)
        except TypeError as ve:
            Esse.printf(f"Got File? TypeError: {ve}\n", RED)
            raise
        self.pith = File.get_pith(self.base)
    
    # Set the encoding for the file (particularly for CSV files)  
    def set_encoding(self):
        with open(self.path, 'rb') as f:
            result = chardet.detect(f.read(SAMPLE_INPUT_SIZE))
            encoding = result['encoding']
        self.encoding = encoding
        
    # Get the pith (aka filename from filename.ext)
    @staticmethod
    def get_pith(basename):
        pith = os.path.splitext(basename)[0]
        return pith
    
    # Find the file with substring (default to csv)
    @staticmethod
    def find_matching_file(directory_path, substring, extension=MAPPING_TYPE):
        # Esse.printf("Find: {substring} Exension: {extension}", YELLOW, substring=substring, extension=extension)    
        files = glob.glob(os.path.join(directory_path, f"*{substring}.{extension}"))
        return files[0] if files else None

# Append Cypher code to template file
class Script(File):
    def generate(self, template_file_path, contents):
        Esse.printf("____________Script: Generate____________\n", GREEN)  
        script_file_path = self.path
        # Replace database 
        # with open(template_file_path, 'r') as template_file:
        ending = 'Esse.printf("...END\\n", RED)'
        with open(script_file_path, 'w') as script_file:
            with open(template_file_path, 'r') as template_file:
                Esse.printf("Generating...", RED)
                script_file.write(template_file.read())
                script_file.write(contents)
                script_file.write(ending)
                Esse.printf("...done", RED)        

# Dictionary Files    
class DictFile(File):
    def __init__(self, path):
        # Don't have to create path here from directory and name as path set in Manifest and being passed here.
        # dict_file_path = dict_file_directory  + "/" + dict_file_name + "." + OUTPUT_PITH
        # self.pith = dict_file_name
        # self.path = dict_file_path
        super().__init__(path)        

    # Use JSON library to dump a dictionary
    def generate(self, map_dict):
        pith = self.pith
        dict_file_path = self.path
        Esse.printf("____________DictFile: Generate {pith}: {dict_file_path}____________\n", GREEN, pith=pith, dict_file_path=dict_file_path)  
        # Esse.printf("\n\n{map_dict}", RED, map_dict=map_dict)
        with open(dict_file_path, 'w') as  dict_file:
            Esse.printf("Generating...", RED)
            json.dump(map_dict, dict_file, indent=4)
            Esse.printf("...done", RED) 
        
# List Files
class ListFile(File):
    def __init__(self, list_file_directory, list_file_name):
        list_file_path = list_file_directory  + "/" + list_file_name + "." + OUTPUT_PITH
        self.pith = list_file_name
        self.path = list_file_path

    # Write node and edge code 
    def generate(self, node_code, edge_code):
        pith = self.pith
        list_file_path = self.path
        Esse.printf("____________ListFile: Generate {pith}: {list_file_path}____________\n", GREEN, pith=pith, list_file_path=list_file_path)  
        content = node_code + edge_code
        with open(list_file_path, 'w') as  list_file:
            Esse.printf("Generating...", RED)
            list_file.write(content)
            Esse.printf("...done", RED) 

# CSV File convenience class
class CSVFile(File):
    def __init__(self, path):
        super().__init__(path)
        self.encoding = self.set_encoding()
    
    # Use Pandas read_csv function to load CSV File
    def ingest(self):
        path = self.path
        encoding = self.encoding
        df = pd.read_csv(path, dtype=str, encoding=encoding)
        return df
    
# Data File classes
class DataFile(CSVFile):
    # Initialize Data File calls File Initialize
    def __init__(self, path):
        super().__init__(path)
        
    # Find the Mapping pattern matching the current file
    def get_file_matching_pattern(self, mapping, phase, aspect):
        pith = self.pith
        aspect_mapping_patterns = mapping.get_aspect_mapping_patterns(phase, aspect)
        
        return next((pattern for pattern in aspect_mapping_patterns if fnmatch.fnmatch(path, pattern)), None)
     
# Directory Class
class Directory(File):
    # Initialize Directory with code and data subdirectories
    # parent trees
    # Instantiate subdirectory, creating if necessary
    def __init__(self, directory, pith, create=False):
        path = os.path.join(directory, pith)
        super().__init__(path)               
        os.makedirs(path, exist_ok=True) if create else None

    # Process the Mapping across all files for the current Phase
    def process(self):
        directory = self.path
        
        Esse.printf("\n____________directory_process____________\n", GREEN)                
        
        mapping = Mapping(directory)
        phase = self.base
        mapping.process(phase)
        
        data_directory = os.path.join(directory, "data")
        data_files = sorted(glob.glob(os.path.join(data_directory, "*.csv")))

        [DataFile(file).process(phase, mapping) for file in data_files]

# Set all of the data file names and their piths
class DataDirectory(Directory):
    def __init__(self, directory, pith, create=False):
        super().__init__(directory, pith)
        path = self.path
        data_file_names =  sorted(glob.glob(os.path.join(path, "*.csv")))
        self.data_file_names = data_file_names
        self.data_files = [CSVFile(data_file_name) for data_file_name in data_file_names]
        self.piths = [csv_file.pith for csv_file in self.data_files]

    def ingest(self):
        dfs = {}
        data_files = self.data_files
        dfs = {csv_file.pith: csv_file.ingest() for csv_file in data_files}
        return dfs

# Transformer for Domain (Cypher or NeoModel)
class Transformer(Esse):
    def __init__(self, manifestation):
        Esse.printf("____________Transformer____________\n", GREEN)                
        # Set the transformer in the manifestation     
        manifestation.transformer = self
        self.manifestation = manifestation
                
# NeoModel Transformer Class
class NeoModel(Transformer):
    def __init__(self, domain):
        Esse.printf("____________NeoModel____________\n", GREEN)                
        super().__init__(domain)

# 3D-Force Graph Transformer Class
class Force(Transformer):
    IDS = set()
    EDGES = set()
    count = 0

    def __init__(self, manifestation):
        super().__init__(manifestation)
        Esse.printf("____________Force____________\n", GREEN)
        # TODO: Multiple Source Files and Abstract Types for Target Files
    
    def handle_projection_case(self, projection, scale):
        top = scale/2
        projection_cases = {
            'flat': lambda: 0,
            'spherical': lambda: random.uniform(-top, 0),
            'hemispherical': lambda: random.uniform(0, top)
        }
        return projection_cases.get(projection, lambda:0)()
    
    def handle_distribution_case(self, distribution, fx, fy, scale):
        fx = float(fx)
        fy = float(fy)
        scale = float(scale)
        distribution_cases = {
            'tight': lambda: (
                fx + random.uniform(-scale * 0.1, scale * 0.1),
                fy + random.uniform(-scale * 0.1, scale * 0.1)
            ),
            'loose': lambda: (
                fx + random.uniform(-scale * 0.5, scale * 0.5),
                fy + random.uniform(-scale * 0.5, scale * 0.5)
            )
        }
        return distribution_cases.get(distribution, distribution_cases[distribution])()

    def id(self, value):
        value = value.replace(',','')
        return value

    def new_id(self, i):
        # Check if the ID has already been seen
        if i in self.IDS:
            return False  # Return None if the ID has been seen before
        else:
            # Add the new ID to the set and return the ID
            self.IDS.add(i)
            return True

    def node(self, node_name, node_df, series):
        # Esse.printf("____________Force: node____________\n", GREEN)

        manifestation = self.manifestation
        manifest = manifestation.manifest
        target_column = manifest.target_column # Attribute or Property
        modality = manifestation.domain.modality
        model = manifestation.domain.model
        domain_type = modality.type
        scale = modality.scale

        # Esse.printf("\nnode_name: {node_name}\n\nseries:\n{series}\n\nnode_df:\n{node_df}\n", BLUE, node_name=node_name, series=series, node_df=node_df)

        # Create node_dict using mappings (rows for properties - id, name)
        node_dict = {
            mapping[target_column]: series[mapping[SOURCE_COLUMN]]
            for _, mapping in node_df.iterrows()
            if mapping[SOURCE_COLUMN] in series
        }
        
        # Check for id
        if 'id' not in node_dict:
            # Esse.printf("{node_name} - NO ID", YELLOW, node_name=node_name)
            return {}  # Return empty dictionary if no ID is present

        # Check if seen
        node_id = node_dict['id']
        if not self.new_id(node_id):
            # Esse.printf("{node_id}: SEEN\n", YELLOW, node_id=node_id)
            return {}  # Return empty dictionary if ID is already seen

        # Add additional properties to the node_dict
        if 'color' in model.globals['Nodes'][node_name]:
            node_dict['color'] = model.globals['Nodes'][node_name]['color']
        if 'size' in model.globals['Nodes'][node_name]:
            node_dict['size'] = model.globals['Nodes'][node_name]['size']

        # If geographic, add orientation 
        if domain_type == 'geographic':
            fx = series['fx']
            fy = series['fy']
            if 'projection' in model.globals['Nodes'][node_name]:
                projection = model.globals['Nodes'][node_name]['projection']
                node_dict['fz'] = self.handle_projection_case(projection, scale)
            if 'distribution' in model.globals['Nodes'][node_name]:
                distribution = model.globals['Nodes'][node_name]['distribution']
                node_dict['fx'], node_dict['fy'] = self.handle_distribution_case(distribution, fx, fy, scale)

        # Dict.printf(node_dict)
        return node_dict  # Return the dictionary directly

    def nodes(self, df, mappings):
        Esse.printf("____________Force: nodes____________\n", RED)

        Dict.printf(mappings)
        DF.printf("File", df)
        
        # Assemble a list of node dictionaries by going through
        # each row (series) in the data file (df)
        # for each node (node_name) and the mapping dataframe for that node (node_df)
        # this will generate all nodes for each row first but it could generate each node for all rows firstif flipped fors
        code = [
            self.node(node_name, node_df, series)
            for node_name, node_df in mappings.items()
            for _, series in df.iterrows()
        ]
          
        # Esse.printf("NODES\n{code}", GREEN, code=code)

        return code

    def seen_edge(self, edge):
        # Check if edge already seen
        # frozenedge = forzenset(edge)
        frozenedge = tuple(sorted(edge.items()))
        if frozenedge in self.EDGES:
            return True
        else:
            # Add the new ID to the set and return the ID
            self.EDGES.add(frozenedge)
            return False

    def edge(self, edge_name, edge_df, series):
        Esse.printf("____________Force: edge____________\n", GREEN)

        manifestation = self.manifestation
        modality = manifestation.domain.modality
        # self.count += 1
        # count = self.count
        # Esse.printf("\n{count} edge: {edge_name}\n\nseries:\n{series}\n\nmappings:\n{edge_df}\n", BLUE, count=count, edge_name=edge_name, series=series, edge_df=edge_df)
        Series.printf(edge_name, series)
        # name: label
        # desc: text
        # source: The id of the source node.
        # target: The id of the target node.
        # color: To specify the color of the link.
        # strength: To specify the strength of the link (which can affect the force simulation).
        edge_dict = {}
        # DF.printf(f"{edge_name}:", edge_df, ['Aspect', 'File', 'Column', 'Node', 'ID', 'Source ID', 'Relationship', 'Target ID'])
        source_node = edge_df['Source Node'].iloc[0]
        source_id = edge_df['Source ID'].iloc[0]
        target_node = edge_df['Target Node'].iloc[0]
        target_id = edge_df['Target ID'].iloc[0]
        relationship = edge_df['Relationship'].iloc[0]

        Esse.printf("Source: {source_node} Target: {target_node} Relationship: {relationship}", BLUE, source_node=source_node, target_node=target_node, relationship=relationship)
            
        if not pd.isna(series[source_id]) and not pd.isna(series[target_id]):            
            edge_dict['name'] = relationship
            edge_dict['source'] = self.id(str(series[source_id]))
            edge_dict['target'] = self.id(str(series[target_id]))           
            edge_dict['color'] = EDGE_COLOR
            edge_dict['strength'] = EDGE_STRENGTH

        if self.seen_edge(edge_dict):
            edge_dict = {}
        
        Dict.printf(edge_dict)

        return edge_dict
        
    # Integrant called from Graph transform method for aspect: edges        
    def edges(self, df, mappings):
        Esse.printf("____________Force: edges____________\n", GREEN)

        Dict.printf(mappings)
        DF.printf("File", df)

        # Assemble a list of edge dictionaries by going through
        # each row (series) in the data file (df)
        # for each edge (edge_name) and the mapping dataframe for that edge (edge_df)
        # this will generate all edges for each row first but it could generate each edge for all rows first if flipped fors
        code = [
            self.edge(edge_name, edge_df, series)
            for edge_name, edge_df in mappings.items()
            for _, series in df.iterrows()
        ]
          
        # Esse.printf("EDGES\n{code}", GREEN, code=code)

        return code    

    def generate(self, master):
        Esse.printf("____________Force: generate____________\n", GREEN)
        manifestation = self.manifestation
        manifest = manifestation.manifest
        dfs = manifest.dfs

        nodes_code = []
        edges_code = []
        
        target_file_path = manifest.target_file_path
        force_file_path = manifest.force_file_path
        
        Esse.printf("Generating Nodes", GREEN)    
        Dict.printf(master['Nodes'])
        
        # Generate Nodes for each file in master['Nodes']
        for file_pith, mappings in master['Nodes'].items():
            Esse.printf(f"\n(Cypher generate) Processing Nodes file: {file_pith}\n", GREEN, file_pith=file_pith)      
            df = dfs[file_pith]
            nodes_code += self.nodes(df, mappings)
            Esse.printf("NODE CODE: {nodes_code}", GREEN, nodes_code=nodes_code) 
        
        Esse.printf("Generating Edges", GREEN)    
        Dict.printf(master['Edges'])

        # Generate Edges for each file in master['Edges']
        for file_pith, mappings in master['Edges'].items():
            Esse.printf(f"\n(Cypher generate) Processing Edges file: {file_pith}\n", GREEN, file_pith=file_pith)
            df = dfs[file_pith]                        
            edges_code += self.edges(df, mappings)
            Esse.printf("EDGE CODE: {edges_code}", BLUE, edges_code=edges_code)    

        map_code = {"nodes": nodes_code, "links": edges_code}     
        Esse.printf("\n\n\n\n\nMAP CODE: {map_code}\n\n\n\n", RED, map_code=map_code)    

        DictFile(target_file_path).generate(map_code)
        DictFile(force_file_path).generate(map_code)
                        
# Cypher Transformer Class
class Cypher(Transformer):

    def __init__(self, manifestation):
        super().__init__(manifestation)
        Esse.printf("____________Cypher____________\n", YELLOW)
        self.manifestation = manifestation
        manifest = manifestation.manifest
        # Copy down the template_file_path and create the Script file object from the target_file_path
        template_file_path = manifest.template_file_path
        target_file_path = manifest.target_file_path
        self.template_file_path = template_file_path
        script = Script(target_file_path) # Cypher file to generate graph
        self.script = script
        
    def get_transform(self, series, column_column):
        column = series[column_column]
        code = f"row.{column}"
        return code
        
    def node_assignments(self, variable_name, node_df):
        Esse.printf("____________Cypher: node_assignments {variable_name}____________\n", YELLOW, variable_name=variable_name)
        manifestation = self.manifestation
        manifest = manifestation.manifest
        target_column = manifest.target_column
                
        code = ""
        if not node_df.empty:
            code += "".join([f"\t\tSET {variable_name}.{row[target_column]} = row.{row[SOURCE_COLUMN]}\n" for index, row in node_df.iterrows()])
        # Esse.printf("{code}", BLUE, code=code)
        return code
    
    def node_set(self, node_name, node_df):
        Esse.printf("____________Cypher: node_set {node_name}____________\n", YELLOW, node_name=node_name)
        # DF.printf(node_name, node_df)
        variable_name = self.get_variable_name(node_name)
        code = ""
        if node_df is not None:
            code += self.node_assignments(variable_name, node_df)
        if code.endswith(","):
            code = code.rstrip(",")
        code += "\n"
        # Esse.printf("{code}", BLUE, code=code)
        return code
    
    def node_merge(self, node_name, id_series):
        Esse.printf("____________Cypher: node_merge {node_name}____________\n", YELLOW, node_name=node_name)
        manifestation = self.manifestation
        manifest = manifestation.manifest
        target_column = manifest.target_column
        source_column = SOURCE_COLUMN
        variable_name = self.get_variable_name(node_name)
        code = ""
        if not id_series.empty:
            #Esse.printf("Series: {id_series}\nSource Column: {source_column} Target Column:{target_column}", RED, id_series=id_series, source_column=source_column, target_column=target_column)
            identifier_transform = self.get_transform(id_series, source_column)
            code += f"\tWITH row\n"
            code += f"\tWHERE {identifier_transform} IS NOT NULL\n"       
            code += f"\tMERGE ({variable_name}:{node_name} "
            code += f"{{id:toString({identifier_transform})}}"   
            code += ")\n"  
        # Esse.printf("{code}", BLUE, code=code)
        return code
    
    def node_body(self, node_name, node_df):
        Esse.printf("____________Cypher: node_body {node_name}____________\n", YELLOW, node_name=node_name)
        manifestation = self.manifestation
        manifest = manifestation.manifest
        target_column = manifest.target_column
        id_property = manifest.id_property
        # Esse.printf("Target Column: {target_column} ID Poperty: {id_property}", YELLOW, target_column=target_column, id_property=id_property)
        code = ""
        # DF.printf(node_name, node_df)
        id_series, redux_df = DF.extract_series(node_name, node_df, target_column, id_property)
        code += self.node_merge(node_name, id_series)
        code += self.node_set(node_name, redux_df)
        # Esse.printf("{code}", BLUE, code=code)
        return code

    def node(self, node_name, node_df):
        Esse.printf("____________Cypher: node {node_name}____________\n", YELLOW, node_name=node_name)
        code = ""
        # DF.printf("node_df", node_df) # Entire Mapping
        code += self.node_body(node_name, node_df)
        # Esse.printf("{code}", BLUE, code=code)
        return code
    
    def nodes_header(self, file_name):
        Esse.printf("____________Cypher: nodes_header____________\n", YELLOW)
        # Esse.printf("{file_name}\n", BLUE, file_name=file_name)
        manifestation = self.manifestation
        manifest = manifestation.manifest
        data_directory_path = manifest.data_directory_path
        source_file_path = os.path.join(data_directory_path, file_name)

        code = ""
        code += f"\n# Loading Nodes from {source_file_path}"
        code += f"\nquery = '''\n"
        code += f"LOAD CSV WITH HEADERS FROM \"file:///{source_file_path}\" AS row\n"
        return code

    def nodes_footer(self):
        code = ""
        code += f"'''"
        code += f"\ngraph.run(query)"
        code += f"\n"
        return code

    def nodes(self, file_pith, file_name, df, mappings):
        """
        Generate Cypher code for nodes in a single file.
        """
        Esse.printf("____________Cypher: nodes____________\n",RED)

        DF.printf("mappings", mappings)

        code = ""
        code += self.nodes_header(file_name)
        code += "".join(
            self.node(node_name, node_df)
            for node_name, node_df in mappings.items()
        )
        code += self.nodes_footer()

        return code

    def edge_line(self, series):
        Esse.printf("____________Cypher: edge_line____________\n", YELLOW)  
        code = ""
        
        Esse.printf("{series}", RED, series=series)
        source_variable = "source"
        source_node = series['Source Node']
        source_identity = series['Source ID']
        target_variable = "target"
        target_node = series['Target Node']
        target_identity = series['Target ID']
        relationship = series['Relationship']
        relationship_property = series['Relationship Property']
        relationship_column = series['Relationship Column']
        
        if Esse.kisn(relationship_column):
            code += "\tMATCH "
            code += f"({source_variable}:{source_node} {{id: toString(row.{source_identity})}}), ({target_variable}:{target_node} {{id: toString(row.{target_identity})}})\n"
            code += "\t\tMERGE"
            code += f"({source_variable})-[edge:{relationship}]->({target_variable})\n"
        else:
            code += "\tMATCH "
            code += f"({source_variable}:{source_node} {{id: toString(row.{source_identity})}}), ({target_variable}:{target_node} {{id: toString(row.{target_identity})}})\n"
            code += "\t\tMERGE"
            code += f"({source_variable})-[edge:{relationship} {{{relationship_property}: toString(row.{relationship_column})}}]->({target_variable})\n"

            # code += "\tMATCH "
            # code += f"({source_variable}:{source_node} {{id: toString(row.{source_identity})}}), ({target_variable}:{target_node} {{id: toString(row.{target_identity})}})\n"
            # code += "\t\tMERGE"
            # code += f"({source_variable})-[edge:{relationship}]->({target_variable})\n"
            # code += f"\t\t\tSET edge.{relationship_property} = toString(row.{relationship_column})"

        # Esse.printf("{code}", BLUE, code=code)
        return code

    def edge_body(self, edge_name, edge_df):
        Esse.printf("____________Cypher: edge_body {edge_name}____________\n", YELLOW, edge_name=edge_name)
        code = ""  
        code += "".join([self.edge_line(series) for _, series in edge_df.iterrows()])
        # Esse.printf("{code}", BLUE, code=code)
        return code

    def edge_header(self, file_name, edge_name):
        Esse.printf("____________Cypher: edge_header____________\n", YELLOW)  
        Esse.printf("{file_name}: {edge_name}\n", BLUE, file_name=file_name, edge_name=edge_name)
        manifestation = self.manifestation
        manifest = manifestation.manifest
        data_directory_path = manifest.data_directory_path
        source_file_path = os.path.join(data_directory_path, file_name)
        
        code = ""
        code += f"\n# Loading Relationships from {source_file_path}"
        code += f"\nquery = '''\n"
        code += f"LOAD CSV WITH HEADERS FROM \"file:///{source_file_path}\" AS row\n"
        # Esse.printf("{code}", BLUE, code=code)
        return code

    def edge_footer(self):
        code = ""
        code += f"'''"
        code += f"\ngraph.run(query)"
        code += f"\n"
        # Esse.printf("{code}", BLUE, code=code)
        return code

    def edge(self, file_name, edge_name, edge_df):
        Esse.printf("____________Cypher: edge____________\n", YELLOW)

        code = ""
        code += self.edge_header(file_name, edge_name)
        code += self.edge_body(edge_name, edge_df)
        code += self.edge_footer()
        # Esse.printf("{code}", BLUE, code=code)
        return code

    def edges(self, file_pith, file_name, df, mappings):
        """
        Generate Cypher code for edges in a single file.
        """
        Esse.printf("____________Cypher: edges____________\n", RED)

        # Generate edge code for each edge mapping
        code = "".join(
            self.edge(file_name, edge_name, edge_df)
            for edge_name, edge_df in mappings.items()
            # for _, series in df.iterrows()
        )

        return code
    
    def generate(self, master):
        """
        Generate Cypher code for each file separately.
        """
        Esse.printf("____________Cypher: generate____________\n", RED)
        manifestation = self.manifestation
        manifest = manifestation.manifest
        dfs = manifest.dfs

        mapping_code = ""
        nodes_code = ""
        edges_code = ""
        
        template_file_path = self.template_file_path
        script = self.script
                
        Esse.printf("Generating Nodes", GREEN)    
        Dict.printf(master['Nodes'])
        
        # Generate Nodes for each file in master['Nodes']
        for file_pith, mappings in master['Nodes'].items():
            Esse.printf(f"\n(Cypher generate) Processing Nodes file: {file_pith}\n", GREEN, file_pith=file_pith)
            file_name = f"{file_pith}.csv"
            df = dfs[file_pith]
            nodes_code += self.nodes(file_pith, file_name, df, mappings)
            Esse.printf("NODE CODE:\n{nodes_code}", GREEN, nodes_code=nodes_code)    
            
        Esse.printf("Generating Edges", GREEN)    
        Dict.printf(master['Edges'])

        # Generate Edges for each file in master['Edges']
        for file_pith, mappings in master['Edges'].items():
            Esse.printf(f"\n(Cypher generate) Processing Edges file: {file_pith}\n", GREEN, file_pith=file_pith)
            file_name = f"{file_pith}.csv"
            df = dfs[file_pith]                        
            edges_code += self.edges(file_pith, file_name, df, mappings)
            Esse.printf("EDGE CODE:\n{edges_code}", GREEN, edges_code=edges_code)   
         
        mapping_code += f"{nodes_code}\n{edges_code}\n"
        Esse.printf("\nMAPPING CODE:\n{mapping_code}\n", BLUE, mapping_code=mapping_code)   
        
        script.generate(template_file_path, mapping_code)
        
        # manifestation.files_code = files_code

# Resource for Domain (Graph or Platform)
class Resource(Esse):
    # Instantiate Platform or Graph    
    def __init__(self, manifestation):
        Esse.printf("____________Resource____________\n", GREEN)
        # Set the resource in the manifestation
        manifestation.resource = self
        self.manifestation = manifestation
                
# Platform Meta Class
class Platform(Resource):
    def __init__(self, domain, transformer):
        Esse.printf("____________Platform____________\n", GREEN)              
        super().__init__(domain, transformer)
                        
    # Generate Platform
    def generate(self):
        Esse.printf("____________Platform: Generate____________\n", GREEN)             

# Graph Meta Class
class Graph(Resource):
    def __init__(self, manifestation):
        super().__init__(manifestation)
        Esse.printf("____________Graph____________\n", YELLOW)

    # Transform given Aspect of the Mapping (Nodes, Edges)
    def transform(self, aspect):
        Esse.printf("____________Graph: Transform {aspect}____________\n", YELLOW, aspect=aspect)
        # Transform the Source Data (Spreadsheet) into this Resource (Graph)
        manifestation = self.manifestation

        # Get the Domain for this Transformation
        domain = manifestation.domain

        # Get the Transformation Mapping from the Domain
        mapping = domain.mapping
        
        # Get the Master mapping df, 
        master = mapping.master

        # Get the Transformer Class (Cypher/Force) and the 
        transformer = manifestation.transformer      
        
        # Get the Transformation (nodes/edges)
        transformation = transformer.get_method_name(aspect)
        
        Esse.printf("TRANSFORM: {transformation}\n", RED, transformation=transformation)
        code = ""   
        try:
            # The nodes or edges instantiated in the appropriate code form for the transformation
            integrant = Esse.extricate(transformer, transformation)
            if not callable(integrant):
                raise ValueError(f"The integrant to instantiation the '{transformation}' aspect does not exist.")
            # Pass master to the transformer (Cypher/Force; nodes/edges) and let it extract Nodes or Edges 
            code = integrant(master)            
        except ValueError as ve:
            Esse.printf(f"ValueError: {ve}", RED)
            raise
        except Exception as e:
            Esse.printf(f"General Error during transformation: {e}", RED)
            raise
            
        return code
   
    # Generate Graph through Transformer Class: Force/Cypher
    def generate(self):
        Esse.printf("____________Graph: Generate____________\n", GREEN)       
        manifestation = self.manifestation
        manifest = manifestation.manifest     
        domain = manifestation.domain
        mapping = domain.mapping
        
        # Transformer Class: Cypher or Force
        transformer = manifestation.transformer

        # Esse.printf("Components:\n", YELLOW)            
        mapping.inspect()
  
        # Get the Master mapping df: files: categories/products, aspects: nodes/edges, specific nodes or edges
        master = mapping.master

        # Transformer class generate method (takes master mapping file as argument)
        generation = transformer.get_method_name(GENERATION_METHOD)

        try:
            # Call Generate Method for specific Transformer (Cypher, Force) with the master
            generate = Esse.extricate(transformer, generation)
            if not callable(generate):
                raise ValueError(f"The generation method: '{generation}' does not exist.")
            # Force.generate
            generate(master)
        except ValueError as ve:
            Esse.printf(f"ValueError: {ve}", RED)
            # Handle specific error, e.g., log, notify, etc.
            raise
        except Exception as e:
            Esse.printf(f"General Error during transformation: {e}", RED)
            # Log error and re-raise or handle accordingly
            raise
               
# Mapping File from which Mapping Data Frame is extracted
class MappingFile(CSVFile):
    def __init__(self, mapping):
        Esse.printf("____________MappingFile:____________\n", GREEN,)          

        # Manifestation <- Domain <- Mapping <- MappingFile          
        mapping.file = self
        self.mapping = mapping

        # ../domain/trees/csv 
        directory_path = mapping.directory_path
                   
        mapping_file_path = File.find_matching_file(directory_path, MAPPING_PITH, MAPPING_TYPE)
        super().__init__(mapping_file_path) 
        Esse.printf("Mapping File: {mapping_file_path}\n", BLUE, mapping_file_path=mapping_file_path)
        
    # Process MappingFile and return Data Frame
    def process(self, mapping):
        Esse.printf("____________MappingFile: Process____________\n", GREEN)          
        path = self.path
        base = self.base
        pith = self.pith
        encoding = self.encoding
        mapping = self.mapping
     
        # Esse.printf("Encoding: {encoding} Path: {path} Base: {base} Pith: {pith}\n", YELLOW, encoding=encoding, path=path, base=base, pith=pith)
        
        # Ingest file through parent CSVFile convenience class       
        df = self.ingest()
        Esse.printf("INGEST: {df}", BLUE, df=df)
        
        # transformer_column
        # Column used for mapping depends on the Transformer - Cypher uses Property, Force uses Attribute
        # Reason for this is am dropping blank values in mapping column for this class in the CSV:
        # e.g. only id and common_name in the Column column are being mapped in the Attribute column (for Force Transformer)
        # height and diameter are not but they are in the Property column (for Cyper Transformer)        
        transformer_column = mapping.transformer_column
        
        df_reduced = df.dropna(subset=[transformer_column])
        Esse.printf("REDUCE: {df_reduced}", BLUE, df_reduced=df_reduced)

        # File Names in order of processing
        data_file_names = DF.unique(df, 'File')
        mapping.data_file_names = data_file_names
        
        return df_reduced

# Mapping defines how mapping is processed
class Mapping(Esse):
    # Initialize Mapping from Directory through Data Frame
    # name, df, Nodes, Edges
    def __init__(self, domain):
        Esse.printf("____________Mapping____________\n", GREEN)

        # Manifestation <- Domain <- Mapping      
        domain.mapping = self
        self.domain = domain
        domain_name = domain.name        
        transformer_class = domain.transformer_class
        manifest = domain.manifest
        # data_directory = manifest.data_directory
        # data_file_names = data_directory.data_file_names
        
        # which column to transform into (attribute for Force or property for Cypher)
        self.transformer_column = manifest.yo['transformer'][transformer_class]['column']

        # Paths
        # ../domain/trees/csv  
        self.directory_path = domain.mapping_path
         
        # Manifestation <- Domain <- Mapping <- MappingFile
        mapping_file = MappingFile(self)
        self.file = mapping_file
        
        # Mapping DF - Aspect, File, Column, Node, Property
        mapping_df = mapping_file.process(self)
        self.df = mapping_df   
        DF.printf(domain_name, mapping_df)

        # File names in the order specified in the mapping df initialized in the MappingFile (set in MappingFile.process)
        # TODO: file_piths
        data_file_names = self.data_file_names
        Esse.printf("File Names in order of processing: {data_file_names}", RED, data_file_names=data_file_names)

        # Split the Mapping up into Nodes and Edges per individual files (by Nodes and Edges)
        self.process()

    def extract_mappings(self, mapping_df):
        """
        Extract unique Nodes and Edges mappings based on modality.

        Args:
            mapping_df (pd.DataFrame): The mapping DataFrame with columns 'Aspect' and 'File'.

        Returns:
            dict: A dictionary with unique keys 'Nodes' and 'Edges', each containing nested dictionaries.
        """
        # Access modality
        domain = self.domain
        model = domain.model
        modality = domain.modality

        # Initialize the result dictionary with sets for uniqueness
        mappings = {'Nodes': set(), 'Edges': set()}

        # Handle the two cases based on modality
        if modality.nominal:
            # Case where 'both' indicates Nodes and Edges are in the same files
            files = set(mapping_df['File'].tolist())
            mappings['Nodes'] = files
            mappings['Edges'] = files
        else:
            # Case where Nodes and Edges are in separate files
            for _, row in mapping_df.iterrows():
                aspect = row['Aspect']
                file = row['File']
                if aspect == 'nodes':
                    mappings['Nodes'].add(file)
                elif aspect == 'edges':
                    mappings['Edges'].add(file)

        # Convert sets to nested dictionaries
        mapping_dict = {key: {file: {} for file in value} for key, value in mappings.items()}
        return mapping_dict

    # Process Data Frame for Mapping by splitting those with all Nodes and only those with Relationships
    def process(self):        
        Esse.printf("\n____________Mapping Process____________", GREEN)
        
        domain = self.domain
        model = domain.model
        modality = domain.modality
                
        # Master mapping df (see Mapping.csv for full list of Columns)
        # Aspect File Column Node Source Node Relationship Target Node
        # both categories categoryName Category 
        # both products productName Product IS_A Category
        # nodes tube
        # edges fromTube toTube
        df = self.df
        
        master = self.extract_mappings(df)
        Esse.printf("\nBEFORE", BLUE)
        Dict.printf(master)

        file_mappings_dfs = DF.split(df, 'File')
            
        master.update({'Nodes': {file_pith: DF.split(file_mappings_dfs[file_pith], 'Node') for file_pith in master['Nodes']}})
        master.update({'Edges': {file_pith: DF.split(file_mappings_dfs[file_pith], 'Relationship') for file_pith in master['Edges']}})
        Esse.printf("\nAFTER", BLUE)
        Dict.printf(master)

        self.master = master
            
# YAML File convenience class
class YAMLFile(File):
    def __init__(self, path):
        super().__init__(path)

    # Use yaml library to load generic YAML file
    def ingest(self):
        path = self.path
        with open(path, 'r') as yaml_file:
            yo = yaml.safe_load(yaml_file)
            
        return yo

# Model File from which all Domain configuration parameters are defined.
class ModelFile(YAMLFile):
    def __init__(self, model):
        Esse.printf("____________ModelFile:____________\n", GREEN)          
    
        # Manifestation <- Domain <- Model <- ModelFile          
        model.file = self
        self.model = model

        # Paths
        # ../domain/trees/yaml    
        directory_path = model.directory_path
        
        model_file_path = File.find_matching_file(directory_path, MODEL_PITH, MODEL_TYPE)
        super().__init__(model_file_path) 
        Esse.printf("Model File: {model_file_path}\n", BLUE, model_file_path=model_file_path)    

# Model defines how nodes and edges are interpreted
class Model(Esse):
    # Initialize Model from Directory through Data Frame
    # name, df, Nodes, Edges
    def __init__(self, domain):
        Esse.printf("____________Model____________\n", GREEN)

        # Get the manifest to load edges if necessary
        manifest = domain.manifest

        # Manifestation <- Domain <- Model      
        domain.model = self
        self.domain = domain
        
        # Paths
        # ../domain/trees/yaml        
        self.directory_path = domain.model_path
        
        # Manifestation <- Domain <- Model <- ModelFile
        model_file = ModelFile(self)
        self.file = model_file
        
        yo = model_file.ingest()
        self.yo = yo            

        self.name = yo['name']
        self.title = yo['title']
        self.description = yo['description']
        self.headline = yo['headline']
                        
        # nodes: color, size; edges: color, strength
        self.globals = {}
        self.globals.update({'Nodes': yo['nodes']})
        self.globals.update({'Edges': yo['edges']})

        Esse.printf("MODEL: {yo}\n", YELLOW, yo=yo)

    def printf(self):
        Esse.print_type(self)
        Esse.printf("MODEL: {self}", RED, self=self)

# Modality File from which processing is defined
class ModalityFile(YAMLFile):
    def __init__(self, modality):
        Esse.printf("____________ModalityFile:____________\n", GREEN)          
    
        # Manifestation <- Domain <- Model <- ModelFile          
        modality.file = self
        self.modality = modality

        # Paths
        # ../domain/trees/yaml    
        directory_path = modality.directory_path
        
        modality_file_path = File.find_matching_file(directory_path, MODALITY_PITH, MODEL_TYPE)
        super().__init__(modality_file_path) 

# Modality specifies whether processing is implicit or explicit (has separate nodes and edges files)
class Modality(Esse):
    # Initialize Model from Directory through Data Frame
    # name, df, Nodes, Edges
    def __init__(self, domain):
        Esse.printf("____________Modality:____________\n", GREEN)          

        # Manifestation <- Domain <- Model      
        domain.modality = self
        self.domain = domain
        manifest = domain.manifest
        self.manifest = manifest
        
        # Paths
        # ../domain/trees/yaml (setup in Domain)
        self.directory_path = domain.modality_path

        # Manifestation <- Domain <- Model <- ModelFile
        modality_file = ModalityFile(self)
        self.file = modality_file               # Files explicit (separate nodes and relationships) or implicit (both)
        
        yo = modality_file.ingest()

        Esse.printf("{yo}\n", RED, yo=yo)

        self.yo = yo
        
        # explicit or nominal
        self.modality = yo['modality']
        
        # geographic or abstract
        self.type = yo['type']
        # scale for graph (only needed for Force so far)
        self.scale = yo['scale']
        modality = yo['modality']
        self.modality = modality

        if modality == EXPLICIT:
            self.explicit = True
            self.nominal = False        
        else:
            self.explicit = False
            self.nominal = True

# Domain contains modality, mapping, and model for domain to be manifested as well as the transformer
class Domain(Esse):
    # Instantiate Domain, adding both Directory and Mapping
    def __init__(self, manifestation):
        Esse.printf("____________Domain____________\n", GREEN)          

        # Manifestation <- Domain
        manifestation.domain = self
        self.manifestation = manifestation
        self.name = manifestation.name
        
        # Transformer Class and Manifest
        self.transformer_class = manifestation.transformer_class # Class of Transformer (Graph or Platform)
        self.manifest = manifestation.manifest
        
        # Paths
        self.directory_path = manifestation.domain_path
        self.model_path = os.path.join(self.directory_path, MODEL_TYPE)    
        self.modality_path = os.path.join(self.directory_path, MODEL_TYPE)   
        self.mapping_path = os.path.join(self.directory_path, MAPPING_TYPE)
        
        # Manifestation <- Domain <- Modality           
        self.modality = Modality(self)

        # Manifestation <- Domain <- Model            
        self.model = Model(self)
        
        # Manifestation <- Domain <- Mapping      
        self.mapping = Mapping(self)
        
# Manifest File from which all configuration parameters are defined.
class ManifestFile(YAMLFile):
    def __init__(self, manifest):
        Esse.printf("____________ManifestFile:____________\n", GREEN)
                
        # Manifestation <- Manifest <- ManifestFile
        manifest.file = self
        self.manifest = manifest
        
        # ../yaml   
        directory_path = manifest.manifest_path
        
        manifest_file_path = File.find_matching_file(directory_path, MANIFEST_PITH, MANIFEST_TYPE)
        super().__init__(manifest_file_path)         
        Esse.printf("Manifest File: {manifest_file_path}\n", BLUE, manifest_file_path=manifest_file_path)

# Manifest holds all directories and paths for source and target
class Manifest(Esse):
    def __init__(self, manifestation):
        Esse.printf("____________Manifest____________\n", GREEN)

        # Manifestation <- Manifest  
        manifestation.manifest = self
        self.manifestation = manifestation
        
        # Get the root directory path and the transformer class from the manifestation
        root_path = manifestation.root_path                  # ../
        domain_name = manifestation.name
        domain_path = manifestation.domain_path              # ../domain/trees
        force_domain_path = manifestation.force_domain_path  # ../vue/public/domain
        transformer_class = manifestation.transformer_class  # Force

        # Set the manifest_path here
        # ../yaml
        self.manifest_path = os.path.join(root_path, MANIFEST_TYPE)
        
        # Get the manifest file
        # ../yaml/manifest.yaml
        manifest_file = ManifestFile(self)
        
        # Set the domain path as the main directory path
        # ../domain/trees
        self.directory_path = domain_path                    # Main directory path for the Domain
        
        # YAML Object will set the directories and constants for the process
        # source: csv
        # target: json
        # input: data
        # output: yada
        # column: Attribute or Property for mapping
        # Assuming Force is the Transformer        
        yo = manifest_file.ingest()
        self.yo = yo

        self.source_pith = yo['transformer'][transformer_class]['source']   # csv
        self.data_pith = yo['transformer'][transformer_class]['input']      # data
        self.target_pith = yo['transformer'][transformer_class]['target']   # json
        self.yada_pith = yo['transformer'][transformer_class]['output']     # json
        self.target_column = yo['transformer'][transformer_class]['column'] # Attribute
        self.id_property = yo['transformer'][transformer_class]['id']       # id

        # SOURCE
        # Directories and Directory Paths
        # ../domain/trees/csv
        source_directory = Directory(self.directory_path, self.source_pith)
        self.source_directory = source_directory

        # DATA DIRECTORY
        # Get the DataDirectory 
        # ../domain/trees/csv/data
        data_directory = DataDirectory(source_directory.path, self.data_pith)
        self.data_directory = data_directory

        # Set its Path
        data_directory_path = data_directory.path
        self.data_directory_path = data_directory_path

        # Ingest the CSV files in the DataDirectory into a dictionary keyed by the file name piths
        dfs = data_directory.ingest()
        List.printf("Piths", data_directory.piths)
        
        # Set the data frames in the Manifest
        self.dfs = dfs
        Dict.printf(dfs)
                                       
        # TARGET
        # ../domain/trees/json
        # ../domain/trees/cy        
        # target_directory_path = self.instantiate(domain_path, self.target_directory_pith)
        # self.target_directory_path = target_directory_path
        target_directory = Directory(domain_path, self.target_pith)
        self.target_directory = target_directory
        target_directory_path = target_directory.path
 
        # Transformer Path
        # ../py/
        transformer_path =  os.path.join(root_path, self.target_pith)
        self.transformer_path = transformer_path
        
        # Template Name
        # Cypher.py
        template_file_name = transformer_class + "." + self.target_pith
        self.template_file_name = template_file_name

        # Template Path
        # ../py/Cypher.py
        template_file_path = os.path.join(transformer_path, template_file_name)
        self.template_file_path = template_file_path
        
        # Target Name
        # trees.json
        # trees.py
        target_file_name = domain_name + "." + self.target_pith # trees.json
        self.target_file_name = target_file_name
        
        # Target Path
        # ../domain/trees/json/trees.json 
        # ../domain/trees/py/trees.py         
        target_file_path = os.path.join(target_directory_path, target_file_name)
        self.target_file_path = target_file_path
        
        # Force Path
        # ../vue/public/domain
        # ../vue/public/domain/trees.json
        force_file_path = os.path.join(force_domain_path, target_file_name)
        self.force_file_path = force_file_path

        Esse.printf("\nData Directory: {data_directory_path}  Output Directory: {target_directory_path}  Target Directory: {target_file_path}\n", BLUE, data_directory_path=data_directory_path, target_directory_path=target_directory_path, target_file_path=target_file_path)

# Manifestation is primary class holding manifest, domain, resource, and transformer.
class Manifestation(Esse):
    def __init__(self, domain_name, resource_class, transformer_class):
        Esse.printf("____________Manifestation____________\n", GREEN)
        """
        Establish all of the paths, resource, and transformer.
        """
        self.name = domain_name                                         # Name of the domain
        self.root_path = ROOT_PATH                                      # ../
        self.domains_path = os.path.join(ROOT_PATH, DOMAIN_PITH)        # ../domain
        self.domain_path = os.path.join(self.domains_path, domain_name) # ../domain/trees
        self.force_domain_path = os.path.join(FORCE_PATH, DOMAIN_PITH)  # ../vue/public/domain
        self.resource_class = resource_class                            # Graph
        self.transformer_class = transformer_class                      # Force
    
        # Manifestation <- ... is the umbrella (Parent) and each Child will set itself and Parent

        # Manifest
        manifest = Manifest(self)
              
        # Domain
        domain = Domain(self)
        
        # Transformer - Either Cypher or Force (3D)
        transformer = Esse.instantiate(transformer_class, self)
        
        # Resource - Always a Graph for now (Platform later)
        resource = Esse.instantiate(resource_class, self)

        # Generate - Either Graph.generate or Force.generate which in turn calls Transformer (Cypher or Force)
        generate = Esse.extricate(resource, GENERATION_METHOD) # generate method for Graph or Platform    
        generate()
    
# Create Domain and Generate Resource (Platform or Graph) and specific type (NeoModel for Platform or Cypher for Graph;)
def main(domain_name, resource_class, transformer_class):
    Esse.printf("____________Main____________\n", GREEN)         
    Esse.printf("Domain: {domain_name}  Resource: {resource_class}  Transformation: {transformer_class}\n", BLUE, domain_name=domain_name, resource_class=resource_class, transformer_class=transformer_class)

    Manifestation(domain_name, resource_class, transformer_class)

if __name__ == '__main__':
    
    Esse.printf("BEGIN...\n", RED)
    parser = argparse.ArgumentParser()
    parser.add_argument('domain_name', help="Domain")
    parser.add_argument('resource_class', help="Resource Class")
    parser.add_argument('transformer_class', help="Transformer Class")
    args = parser.parse_args()
    main(args.domain_name, args.resource_class, args.transformer_class)
    Esse.printf("\n...END", RED)

# pushd ~/radialnexus/py
# python3 manifest.py tube Graph Force
# python3 manifest.py tube Graph Cypher
# python3 manifest.py northwind Graph Force
# python3 manifest.py northwind Graph Cypher
#
# Older single-file calls
# python3 manifest.py northwind Graph Force manifest
# python3 manifest.py tube Graph Force london_transport_datasets_London_stations_edited
# python3 manifest.py manifest Graph Cypher manifest
# python3 manifest.py manifest Graph Force manifest
# python3 manifest.py trees Graph Force Exceptional_Trees_On_Oahu
# python3 manifest.py trees Graph Cypher Exceptional_Trees_On_Oahu


      



        
