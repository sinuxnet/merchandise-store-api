# Base image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variables
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_NAME=merchandise-store
ENV DB_USER=db_user
ENV DB_PASSWORD=PostgresP@ssw0rd

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
