# Use Python 3.9 slim as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Download the spaCy model
RUN python -m spacy download en_core_web_sm

# Download NLTK resources
RUN python -m nltk.downloader words && \
    python -m nltk.downloader stopwords

# Copy the rest of your application code into the container
COPY . .

# Move main.py from the src folder to the working directory and remove it from src
RUN mv src/main.py .

# Set the default command to run your application
CMD ["python", "main.py"]
