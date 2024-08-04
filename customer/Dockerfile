FROM python:3.10.12-bullseye

WORKDIR /app/customer

# Copy the application code
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama
RUN curl -L https://ollama.com/install.sh | bash

# Make scripts executable
RUN chmod +x wait-for-it.sh
RUN chmod +x run-ollama.sh

# Expose the necessary port
EXPOSE 11434

ENV PYTHONPATH="${PYTHONPATH}:/app/customer:"

ENTRYPOINT ["./wait-for-it.sh", "redis:6379", "--", "./run-ollama.sh"]
CMD ["python", "./customer_agent.py"]
