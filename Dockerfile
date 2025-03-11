# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project
COPY . .

# Create directories for data if they don't exist
RUN mkdir -p data/raw_files

# Default command to run the Scrapy spider
CMD ["scrapy", "crawl", "wb_repro"]
