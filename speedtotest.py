import speedtest
from colorama import Fore, init

# Initialize colorama for colored output
init(autoreset=True)  # Automatically reset color after each print statement

# Function to run speedtest and display results
def run_speedtest():
    """
    This function runs the speedtest to measure download and upload speeds.
    It handles errors gracefully and displays the results in a colorized format.
    """
    try:
        st = speedtest.Speedtest()  # Create a Speedtest object to interact with the speedtest server
        st.get_best_server()  # Get the best server based on ping

        # Get the download and upload speeds (in Mbps)
        download_speed = st.download() / 1_000_000  # Convert bytes to Megabits
        upload_speed = st.upload() / 1_000_000      # Convert bytes to Megabits

        # Print results with colors for better readability
        print(f"\n{Fore.CYAN}Speedtest Results:{Fore.RESET}")  # Section header
        print(f"{Fore.GREEN}Download Speed: {download_speed:.2f} Mbps{Fore.RESET}")  # Display download speed
        print(f"{Fore.YELLOW}Upload Speed: {upload_speed:.2f} Mbps{Fore.RESET}")  # Display upload speed

    except speedtest.ConfigRetrievalError as e:
        # Handle specific error where the server configuration cannot be retrieved
        print(f"{Fore.RED}[ERROR] Speedtest failed: HTTP Error 403: Forbidden. This might be due to network restrictions or rate limiting.{Fore.RESET}")
    except Exception as e:
        # Handle any other unforeseen errors
        print(f"{Fore.RED}[ERROR] Speedtest failed: {str(e)}{Fore.RESET}")
