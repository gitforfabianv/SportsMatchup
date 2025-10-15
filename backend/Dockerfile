# Use the official Python 3.13 slim image as the base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker caching
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend directory files into the working directory
COPY . .

# Expose the port that Flask will run on (default is 5000)
EXPOSE 5000

# Set environment variable for Flask app (assuming the entrypoint file is named app.py; adjust if different)
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]