FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    solc \
    nodejs \
    npm

# Install Slither
RUN pip3 install slither-analyzer

# Your app setup
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Command to run app
CMD ["python", "app.py"]