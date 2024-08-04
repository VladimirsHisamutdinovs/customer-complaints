#!/bin/bash

# Start Ollama server
ollama serve &

# Wait for Ollama server to be ready
until ollama list | grep "NAME"; do
  sleep 1
done

# Pull the necessary model
ollama pull phi3

# Execute the original command
exec "$@"
