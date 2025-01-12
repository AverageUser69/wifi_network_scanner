import subprocess

# Import discovery and speedtest modules at the top level
try:
    import discovery  # Importing discovery module to handle network device scanning
except ImportError:
    discovery = None
    print("Error: discovery.py is missing.")  # Error message if discovery module is missing

try:
    import speedtotest  # Importing the custom speedtest module for network speed testing
except ImportError:
    speedtotest = None
    print("Error: speedtotest.py is missing.")  # Error message if speedtotest module is missing

# Function to get the IP address and subnet mask of the Wi-Fi adapter
def get_ip_and_subnet():
    """
    Runs the 'ipconfig' command to retrieve the current network configuration.
    Specifically, it looks for the Wi-Fi adapter to extract the IP address and subnet mask.
    """
    # Run the 'ipconfig' command (works on Windows) to get network configuration
    ip_address = subprocess.check_output("ipconfig", shell=True).decode()

    # Variables to store the IP and subnet mask
    ip = None
    subnet_mask = None
    wifi_found = False  # Flag to indicate when the Wi-Fi section is found

    # Loop through each line in the 'ipconfig' output
    for line in ip_address.split("\n"):
        # Look for the Wi-Fi adapter section
        if "Wireless LAN adapter Wi-Fi" in line:
            wifi_found = True
        
        # Extract the IPv4 address and subnet mask if Wi-Fi adapter is found
        if wifi_found:
            if "IPv4 Address" in line:
                ip = line.split(":")[1].strip()
            if "Subnet Mask" in line:
                subnet_mask = line.split(":")[1].strip()

            # Once both IP and subnet mask are found, break out of the loop
            if ip and subnet_mask:
                break

    return ip, subnet_mask

# Function to adjust the IP address based on the subnet mask
def adjust_ip(ip, subnet_mask):
    """
    Adjusts the IP address to match the subnet mask. This function ensures that
    the host part of the IP address is set to 0 based on the subnet mask.
    """
    ip_parts = ip.split(".")
    subnet_parts = subnet_mask.split(".")

    # Modify the IP based on the subnet mask
    for i in range(4):
        if subnet_parts[i] == "255":
            continue
        else:
            ip_parts[i] = "0"
            break

    return ".".join(ip_parts)  # Returns the adjusted IP address

# Function to send IP address to other scripts
def send_ip(ip):
    """
    Sends the adjusted IP to discovery and speedtest scripts for further processing.
    """
    if discovery:
        discovery.print_ip(ip)  # Sending IP to the discovery module for device scanning
    if speedtotest:
        speedtotest.run_speedtest()  # Running speedtest from the speedtotest module

# Main script logic to get IP and subnet, adjust the IP, and pass it to other scripts
if __name__ == "__main__":
    ip, subnet_mask = get_ip_and_subnet()  # Retrieve the IP and subnet mask

    if ip and subnet_mask:
        # Adjust the IP based on the subnet mask
        adjusted_ip = adjust_ip(ip, subnet_mask)
        send_ip(adjusted_ip)  # Send the adjusted IP for further processing
    else:
        print("No valid Wi-Fi IP address or subnet mask found.")  # Error if no valid IP is found
