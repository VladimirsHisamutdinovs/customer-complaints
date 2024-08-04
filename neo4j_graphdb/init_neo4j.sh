#!/bin/bash

# Wait for Neo4j to be ready
until cypher-shell -u neo4j -p password "RETURN 1" > /dev/null 2>&1; do
  echo "Waiting for Neo4j to be ready..."
  sleep 5
done

# Create the complaints database
cypher-shell -u neo4j -p password "CREATE DATABASE complaints"
