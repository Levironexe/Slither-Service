FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    python3-pip \
    nodejs \
    npm

# Install Solidity compiler
RUN curl -fsSL https://bootstrap.pypa.io/get-pip.py | python3
RUN pip3 install --user solc-select
RUN pip3 install solidity-utils
RUN solc-select install 0.8.0
RUN solc-select use 0.8.0

# Install Slither
RUN pip3 install slither-analyzer

# Your app setup
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Command to run app
CMD ["python", "app.py"]