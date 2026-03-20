import os
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
# from py2neo import Graph, Node, Relationship
# from dotenv import load_dotenv
from neo4j import GraphDatabase

# Constants
RED = "31;1"
GREEN = "32;1"
YELLOW = "33;1"
BLUE = "34;1"

NEO4J_BASE_URL = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "Sc1Mitar!"
NEO4J_DATABASE = "tube"

# load_dotenv()

# Meta class for all classes
class Esse:
    # Print Formatted String with Keywords
    @staticmethod
    def printf(formatted_text, code, **kwargs):
        print(f"\033[{code}m{formatted_text.format(**kwargs)}\033[0m")

class GraphDB:
    def __init__(self, uri, user, password, database):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._database = database
        self._uri = uri
    
    def close(self):
        self._driver.close()
        
    def run(self, query):
        database = self._database
        uri = self._uri
        Esse.printf("QUERY: ({database}:\n{query})", BLUE, database=database, query=query)
        with self._driver.session(database=database) as session:
            results = session.run(query)
            return results

def delete_all_nodes(graph):
    graph.run("MATCH (n) DETACH DELETE n")
    
def delete_all_edges(graph):
    graph.run("MATCH ()-[r]-() DELETE r")    

def main(graph):
    
    delete_all_nodes(graph)
    delete_all_edges(graph)

if __name__ == '__main__':

    Esse.printf("BEGIN...\n", RED)
    # neo4j_url = os.environ["NEO4J_BASE_URL"]
    # neo4j_user = os.environ["NEO4J_USERNAME"]
    # neo4j_pass = os.environ["NEO4J_PASSWORD"]
    # neo4j_db = os.environ["NEO4J_DATABASE"]
    
    neo4j_url = NEO4J_BASE_URL
    neo4j_user = NEO4J_USERNAME
    neo4j_pass = NEO4J_PASSWORD
    neo4j_db = NEO4J_DATABASE
    
    Esse.printf("URL: {neo4j_url} USER: {neo4j_user} DB: {neo4j_db}", BLUE, neo4j_url=neo4j_url, neo4j_user=neo4j_user, neo4j_db=neo4j_db)

    # graph = Graph(neo4j_url, auth=(neo4j_user, neo4j_pass))
    graph = GraphDB(neo4j_url, neo4j_user, neo4j_pass, neo4j_db)
    
    main(graph)
# Loading Nodes from ../domain/tube/csv/data/london_transport_datasets_London_stations_edited.csv
query = '''
LOAD CSV WITH HEADERS FROM "file:///../domain/tube/csv/data/london_transport_datasets_London_stations_edited.csv" AS row
	WITH row
	WHERE row.Station IS NOT NULL
	MERGE (station:Station {id:toString(row.Station)})
		SET station.name = row.Station

'''
graph.run(query)


# Loading Relationships from ../domain/tube/csv/data/london_transport_datasets_London_tube_lines.csv
query = '''
LOAD CSV WITH HEADERS FROM "file:///../domain/tube/csv/data/london_transport_datasets_London_tube_lines.csv" AS row
	MATCH (source:Station {id: toString(row.From_Station)}), (target:Station {id: toString(row.To_Station)})
		MERGE(source)-[edge:Tube_Line {name: toString(row.Tube_Line)}]->(target)
'''
graph.run(query)

