# Use an official Python runtime
FROM python:3.8-slim

# Install dependencies directly
RUN pip install --no-cache-dir kafka-python pulp pandas numpy matplotlib

WORKDIR /app

# Copy your Python scripts only
COPY kafka_producer.py backtest.py ./

# Mount point for your CSV
VOLUME ["/data"]

# Keep the container alive until overridden by docker-compose
CMD ["sleep", "infinity"]
