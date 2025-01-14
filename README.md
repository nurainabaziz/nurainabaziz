# Traffic Analysis

This project analyzes web traffic logs, generates insights, and plots various traffic metrics. It includes Docker support for easy setup and deployment.

# Data Pipeline Design Documentation 

I've shared the data pipeline architecture using Airflow with the diagram provided. Capture.PNG

## Requirements

- Docker

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/nurainabaziz/webtraffic.git
    cd webtraffic
    ```

2. Build the Docker image:
    ```bash
    docker build -t webtraffic .
    ```

3. Run the Docker container:
    ```bash
    docker run -v $(pwd)/data:/app/data webtraffic
    ```

## Usage

- Place your web traffic log file in the `data` directory.
- The script will read the logs, analyze them, and generate output files in the `data` directory.

## Output

- The cleaned log data will be saved as `cleaned_logs.csv`.
- Data visualization screenshots are saved as PNG files in the `output` directory.
  

## Author

- Nur Ain Ab Aziz
