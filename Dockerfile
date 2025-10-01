# Step 1: Use an official Python image as a base image.
# A 'slim' version is chosen because it's lighter than the full one.
FROM python:3.11-slim

# Step 2: Set the working directory inside the container.
# All subsequent actions (copying, running) will be relative to this path.
WORKDIR /app

# Step 3: Install the pytest dependency.
# To simplify, we install it directly instead of using a requirements.txt file.
RUN python3 -m pip install --no-cache-dir pytest

# Step 4: Copy the project files to the working directory.
# The test script and the data folder are copied.
COPY test_data_validation.py .
COPY data/ ./data/

# Step 5: Define the command that will run when the container starts.
# This is the command you requested to run the tests.
CMD ["python3", "-m", "pytest", "-v"]