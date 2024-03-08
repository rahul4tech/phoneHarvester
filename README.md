# Phone Harvester

Phone Harvester is a Python script that extracts phone numbers from multiple CSV files and combines them into a single CSV file.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- Python 3
- pandas library
- Git (for cloning the repository)

### Installation

1. Clone the repository
2. cd into the repository
3. Run the following command to install the required libraries:
```sh
pip install -r requirements.req
```

## Usage
Put all the CSV files you want to extract phone numbers from in the `input` folder. Then run the following command:
```sh
python phoneHarvester.py
```
The script will then extract all the phone numbers from the CSV files and combine them into a single CSV file in the `output` folder.
