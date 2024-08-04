FROM python:3.10.12-bullseye

# Set the working directory in the container
WORKDIR /app/timeseries_generator

# Copy the requirements file into the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container


# Command to run the application
CMD ["python", "app.py"]