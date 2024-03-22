# Network Scanner

## Overview
This Python project is a simple network scanner that allows you to discover devices on your local network.
It utilizes the `pysnmp` library for SNMP (Simple Network Management Protocol) functionality and `wakeonlan` for waking up devices using Wake-on-LAN.

## Requirements
- Python 2.7
- `pysnmp` library (install via `pip install pysnmp`)
- `wakeonlan` library (install via `pip install wakeonlan`)

## Installation
1. Clone or download the repository to your local machine.
2. Install the required libraries using pip:
    ```
    pip install pysnmp
    pip install wakeonlan
    ```

## Usage
1. Navigate to the directory where the project is located.
2. Run the `scan_all.py` script:
    ```
    python scan_all.py
    ```
3. Follow the on-screen instructions to scan the network and perform various actions like discovering devices or waking them up using Wake-on-LAN.

## Features
- Discover devices on the local network.
- Retrieve information about discovered devices using SNMP.
- Wake up devices using Wake-on-LAN functionality.
