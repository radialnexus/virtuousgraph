# Virtuous Graph

This is the code base for the "Virtuous Graph" initiative (virtuousgraph.com).  The Virtuous Graph motto is Graph as Code; Code as Graph.  The goal is to implement our vision of programming: taking a graph-centric approach to programming itself - to visualize the program as a graph and ultimately to modify a graph to modify a program.

To start, we want to make it easy as possible to transform data sets (in their ubiquitous CSV format) into various resources for interacting with those data sets.  The initial focus is on manifesting Graphs themselves in a variety of representations, specifically to start as either Neo4j Graph Database or interactive 3D graphs.

These data sets can be anything from a set of RGB Color Codes to Exceptional Trees in Hawaii.  All of these CSV files originate from a "Domain of Discourse".  The Domain defines the subject matter; the Discourse your interaction with the subject.  To start, we instantiate a domain - take your CSV file and define two assets for transforming data into graph:

Mapping
Model

The Mapping CSV file defines what values in the CSV file columns are mapped to what Nodes, Edges and associated Properties.  The Model YAML file defines a set of overall attributes relative to the Mappping, such as what color which Nodes should be presented in a 3D view of the graph, for example.

To manifest a graph from the data you need to instantiate your domain using your Domain Data Spreadsheet.  A sample data spreadsheet is provided in sor.
Use domain.csv as an example.

pushd ~/radialnexus/py
python3 instantiate.py manifest
cp domain.csv manifest/csv/data
mv domain.csv manifest.csv
python3 manifest.py manifest Graph Force manifest

Update domain.yaml
	name: code
	title: Code
	headline: Code
	description: Code

## Domain

Get your data spreadsheet.  


Usage:

	python3 manifest.py trees Graph Cypher Exceptional_Trees_On_Oahu

Parameters: Here's an explanation of the parameters above

    trees:      the top-level directory containing the Domain of Discourse
    Graph:      the desired Manifestation
    Cypher:     the required Transformation
    Source:     the current Source

Structure:  Here's the overall structure

    domains/
        trees/
		colors/
		<domain>/
			csv/
			xls/
	py/
		manifest.py
	vue/
	yaml/
	
Extension:	Here's adding a new domain (journeys)

From installation directory (radialnexus):

cd domain
mkdir journeys; cd journeys
mkdir xls; cd xls
cp ../../colors/xls/00_Mapping.xls .;
Edit Excel to define mapping 
Make sure using Attribute for Force and Property for Graph
Save in CSV format to (new) csv subdirectory (00_Mapping.csv)
Create data/ in csv and add data file matching mapping
Create yaml/ in journeys and create 00_Model.yaml (use trees as template)
Make sure no tabs in the damn yaml file
Make sure domain/json directory exists!
THEN go over to vue directory
copy domain.json over to vue/public/domain
copy views/TreesGraph.vue to views/domainGraph.vue and edit
	id
	name
	fetch
edit main.js
	import domainGraph.vue
	routes
	
Install
	npm
	3D Graph
	

Initialization:

Install a Desktop version of Neo4j.  Then add to your shell profile:

    export NEO4J_USERNAME=neo4j
    export NEO4J_PASSWORD=<pwd>
    export NEO4J_BOLT_URL="bolt://$NEO4J_USERNAME:$NEO4J_PASSWORD@localhost:7687"
    export NEO4J_BASE_URL="bolt:/localhost:7687"

Structure:  Here's the directory structure the example currently assumes

    domains/
        trees/
            02_Mapping.csv
            csv/
                data/
                info/
            json/
            py/
	py/
		manifest.py
	vue/
	xls/
	yaml/

From the py subdirectory parallel to domains, run the method as follows:

    python3 manifest.py trees Graph Cypher Exceptional_Trees_On_Oahu

Then in the py subdirectory there will be 

    <domain>.py 

script generated.  Run that script:

    python3 <domain>.py

to load the graph.  Share and Enjoy.

Intention: 

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

Notes:

Manifest provides provenance and is optional.


Copyright(c), 2023, Michael Bauer.  All Rights Reserved.

