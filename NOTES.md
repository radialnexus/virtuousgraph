# Development Notes

Working notes from development. See README.md for the canonical project documentation.

## Paths

Original development path was `~/radialnexus/py`.

## Adding a New Domain (detailed walkthrough)

From installation directory:

```
cd domain
mkdir journeys; cd journeys
mkdir xls; cd xls
cp ../../colors/xls/00_Mapping.xls .
```

Edit Excel to define mapping:
- Use `Attribute` for Force and `Property` for Graph
- Save in CSV format to (new) csv subdirectory (00_Mapping.csv)

```
mkdir -p csv/data
```

Add data file matching mapping to `csv/data/`.

Create yaml:
```
mkdir yaml
```
Create `yaml/00_Model.yaml` (use trees as template).
Make sure no tabs in the yaml file.

Make sure `domain/json` directory exists.

Then go over to vue directory:
- Copy `domain.json` over to `vue/public/domain/`
- Copy `views/TreesGraph.vue` to `views/domainGraph.vue` and edit:
  - id
  - name
  - fetch path
- Edit `main.js`:
  - Import the new component
  - Add route

## Neo4j Setup

Install a Desktop version of Neo4j. Then add to your shell profile:

```
export NEO4J_USERNAME=neo4j
export NEO4J_PASSWORD=<pwd>
export NEO4J_BOLT_URL="bolt://$NEO4J_USERNAME:$NEO4J_PASSWORD@localhost:7687"
export NEO4J_BASE_URL="bolt:/localhost:7687"
```

## Instantiation Shorthand

```
pushd ~/radialnexus/py
python3 instantiate.py manifest
cp domain.csv manifest/csv/data
mv domain.csv manifest.csv
python3 manifest.py manifest Graph Force manifest
```

Update domain.yaml:
```yaml
name: code
title: Code
headline: Code
description: Code
```

## Manifest Provenance

Manifest provides provenance and is optional.

## Notes

- Mapping CSV file defines what values in the CSV file columns are mapped to what Nodes, Edges and associated Properties.
- Model YAML file defines a set of overall attributes relative to the Mapping, such as node colors for 3D view.
- The key differentiating point for the script is its integration of the Graph into the Code and its view of Code as a Graph. Inheritance is used, with Classes corresponding to parameters so that the specific Transformer can be specified and executed against.

Copyright(c), 2023, Michael Bauer. All Rights Reserved.
