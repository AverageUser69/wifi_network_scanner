import subprocess
import threading
import socket
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Lock for ensuring print happens in a thread-safe way
print_lock = threading.Lock()

# Function to perform a network scan using ping and ARP
def network_scan(ip_range):
    devices = []
    threads = []
    
    # Ping all IPs in the range (This assumes /24 subnet for simplicity)
    for i in range(1, 255):
        ip = f"{ip_range}.{i}"
        thread = threading.Thread(target=ping_device, args=(ip, devices))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return devices

# Function to ping a device and if successful, get its MAC address
def ping_device(ip, devices):
    try:
        response = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # If the ping was successful, try to get the MAC address using ARP
        if response.returncode == 0:
            mac = get_mac_address(ip)
            hostname = get_device_name(ip)
            device_info = {
                'IP Address': ip,
                'MAC Address': mac if mac else 'N/A',
                'Hostname': hostname if hostname else 'N/A'
            }
            
            # Lock for thread-safe print and adding to devices list
            with print_lock:
                devices.append(device_info)

    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to ping {ip}: {str(e)}")

# Function to get the MAC address of a device using ARP
def get_mac_address(ip):
    try:
        # Run the 'arp -a' command to get the MAC address for a given IP
        arp_output = subprocess.check_output(['arp', '-a', ip]).decode()
        # Extract the MAC address from the output
        mac = None
        for line in arp_output.splitlines():
            if ip in line:
                # Extract MAC address from the line
                mac = line.split()[1]  # The MAC address is at the second position in the line
                if mac:
                    return mac
        return "N/A"
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to get MAC address for {ip}: {str(e)}")
        return "N/A"

# Function to try and get the hostname of a device from its IP address
def get_device_name(ip):
    try:
        # Perform a reverse DNS lookup to get the device name
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return None  # If the device name is not available

# Function to scan the network based on the given IP
def print_ip(ip):
    print(Fore.GREEN + f"Discovery Script received IP: {ip}")
    
    # Get the network range dynamically based on the subnet mask
    network_range = '.'.join(ip.split('.')[:3])  # Default to /24 subnet for now
    
    print(Fore.YELLOW + f"Scanning network {network_range}.* for devices...\n")
    
    try:
        # Perform network scan using ping and ARP
        devices = network_scan(network_range)
        
        if not devices:
            print(Fore.RED + "No devices found on the network.")
        else:
            print(Fore.GREEN + "\nDevices found on the network:")
            # Prepare the table rows
            headers = ['IP Address', 'MAC Address', 'Hostname']
            table_data = []

            # Add the cyan-colored first row
            first_row = devices[0]
            first_row_colored = [Fore.CYAN + first_row['IP Address'], Fore.CYAN + first_row['MAC Address'], Fore.CYAN + first_row['Hostname']]
            table_data.append(first_row_colored)

            # Add the rest of the rows in green
            for device in devices[1:]:
                row = [Fore.GREEN + device['IP Address'], Fore.GREEN + device['MAC Address'], Fore.GREEN + device['Hostname']]
                table_data.append(row)

            # Print the table with custom color for the first row
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    except Exception as e:
        print(Fore.RED + f"[ERROR] Network scan failed: {str(e)}")

# Adding Module Import Error Handling
try:
    import subprocess
    import threading
    import socket
    from tabulate import tabulate
    from colorama import Fore, Style, init
except ImportError as e:
    print(Fore.RED + f"[ERROR] Missing required module: {str(e)}")
    exit(1)
