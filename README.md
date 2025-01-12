# Wi-Fi Network Scanner

This project scans the local network to identify connected devices and then runs a speed test to check the network's download and upload speeds. It is implemented using Python and relies on the `speedtest-cli` library for network speed testing and a custom discovery script for identifying devices on the local network.

## Features

- Scans the local network for connected devices (IP address, MAC address, and hostname).
- Runs a speed test to check the current network download and upload speeds.
- Outputs results in a formatted, colorized way with clear error handling.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/wifi_network_scanner.git
   ```

2. Navigate into the project directory:

   ```bash
   cd wifi_network_scanner
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   **Note**: If you encounter issues with the speedtest-cli, ensure you have the required dependencies installed for your platform.

## Running the Script

To run the network scanner and speed test, simply execute the `main.py` script:

```bash
python main.py
```

The script will:

1. Retrieve your local machine's IP address and subnet mask.
2. Adjust the IP address based on the subnet mask.
3. Scan the local network for devices and display a list with device information.
4. Run a speed test to measure download and upload speeds.

## Expected Output

The output is colorized and clearly separated into sections for better readability. Here's an example of what you might see when running the script:

![image](https://github.com/user-attachments/assets/8c1456ea-f0d4-456c-a9b9-eb901fba598a)

### Explanation of Output

#### Discovery Section

- **Discovery Script received IP**: The script starts by detecting your current IP address on the local network.
- **Scanning network 192.168.1.\***: The script then scans the local subnet (e.g., 192.168.1.*) for devices connected to the network.
  
**Devices found on the network**:

- The script lists the **IP address**, **MAC address**, and **hostname** of each device found on the local network.
  
  Devices with the same IP but no hostname or MAC address (N/A) indicate devices that are not fully identified.

#### Speedtest Section

- **Speedtest Results**: After scanning the network, the script performs a speed test and outputs the results.
  
  Example:
  - `Download Speed: 49.17 Mbps`: Indicates the speed at which your network can download data.
  - `Upload Speed: 26.49 Mbps`: Indicates the speed at which your network can upload data.

---

## Error Handling

The script also handles errors in a user-friendly manner. For example:

1. **Missing Files**: If the `discovery.py` or `speedtotest.py` file is missing, an error message is displayed.
2. **Speedtest Errors**: If there’s an issue with the speed test (e.g., the server configuration cannot be retrieved), a helpful error message is shown.
3. **Network Errors**: If the network scan cannot be completed, appropriate messages will inform the user.

## Requirements

- Python 3.x
- `speedtest-cli` (for running the speed test)
- `colorama` (for colorizing the output)

To install these dependencies, run:

```bash
pip install speedtest-cli colorama
```
