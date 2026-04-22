# Virtuous Graph

**Graph as Code; Code as Graph.**

Virtuous Graph takes a graph-centric approach to programming: visualize a program as a graph, modify the graph to modify the program. It transforms data sets in CSV format into interactive 3D graph visualizations and Neo4j graph databases through a declarative mapping and model system.

## Quickstart

Prerequisites: Python 3, Node.js, npm.

```bash
# Install Python dependencies
pip install pandas numpy chardet pyyaml unidecode

# Generate the 3D force graph for Hawaiian Trees
cd py
python3 manifest.py trees Graph Force Exceptional_Trees_On_Oahu

# Copy the output to the Vue app
cp ../domain/trees/json/trees.json ../vue/public/domain/

# Install and run the Vue app
cd ../vue
npm install
npm run serve
```

Open http://localhost:8080/trees to see exceptional trees on Oahu self-organize into the Hawaiian island chain through force-directed layout.

## How It Works

Every data set belongs to a **Domain of Discourse** -- the subject matter and your interaction with it. Each domain defines two assets:

- **Mapping** (`csv/00_Mapping.csv`) -- maps CSV columns to graph Nodes, Edges, and Properties
- **Model** (`yaml/00_Model.yaml`) -- defines presentation attributes like node colors, sizes, and spatial distribution

The `manifest.py` script reads these definitions and transforms source data into a target representation through a **Transformer**. The transformer is specified as a class parameter, making the code structure mirror the graph structure -- classes correspond to graph concepts, inheritance defines the transformation hierarchy.

```
manifest.py <domain> <resource> <transformer> <source>
```

| Parameter | Description | Examples |
|-----------|-------------|----------|
| domain | Directory containing the Domain of Discourse | `trees`, `colors`, `tube` |
| resource | The desired output resource | `Graph` |
| transformer | The transformation method | `Force` (3D), `Cypher` (Neo4j) |
| source | The source data file (without .csv) | `Exceptional_Trees_On_Oahu` |

## Project Structure

```
virtuousgraph/
    domain/                 # Domains of Discourse
        trees/              # Hawaiian exceptional trees
            csv/            # Mapping and source data
                data/       # CSV data files
            json/           # Generated graph JSON
            yaml/           # Model and modality definitions
        colors/             # RGB color codes
        tube/               # London Underground
    py/                     # Core Python scripts
        manifest.py         # Graph manifestation engine
        instantiate.py      # Domain scaffolding tool
        Cypher.py           # Neo4j Cypher template
    vue/                    # Vue 3 frontend
        src/
            views/          # Graph view components
        public/
            domain/         # Graph JSON served to frontend
    yaml/                   # Global manifest configuration
```

## Domains

Three example domains are included:

| Domain | Data | What it shows |
|--------|------|---------------|
| trees | Exceptional Trees on Oahu | Geographic nodes self-organize into Hawaiian island clusters |
| colors | RGB Color Codes | Color relationships in 3D space |
| tube | London Underground | Transit network as a graph |

## Adding a New Domain

1. Scaffold the directory structure:
   ```bash
   cd py
   python3 instantiate.py <domain_name>
   ```

2. Add your CSV data to `domain/<name>/csv/data/`.

3. Define the mapping in `domain/<name>/csv/00_Mapping.csv` (use `trees` as a template).

4. Define the model in `domain/<name>/yaml/00_Model.yaml` (node colors, sizes, layout).

5. Generate the graph:
   ```bash
   python3 manifest.py <name> Graph Force <source>
   ```

6. Copy the JSON output to the Vue app and add a view component and route (see [NOTES.md](NOTES.md) for detailed steps).

## Neo4j (Optional)

To generate Cypher scripts for loading into Neo4j:

```bash
python3 manifest.py trees Graph Cypher Exceptional_Trees_On_Oahu
python3 domain/trees/py/trees.py
```

Requires Neo4j Desktop with connection environment variables configured. See [NOTES.md](NOTES.md) for setup.

## Vision

The key differentiating point is the integration of the Graph into the Code and the view of Code as a Graph. Inheritance is used, with classes corresponding to graph parameters so that the specific Transformer can be specified and executed against. The graph is not just a data structure to be queried -- it is the program.

This prototype demonstrates the concept with data transformation. The larger vision is an **intelligent graph** where traversal triggers executable behavior: nodes carry code, edges define execution flow, and side effects during traversal connect the graph to external systems and data sources in real time.

## License

Copyright (c) 2023, Michael Bauer. All Rights Reserved.
