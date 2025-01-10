import platform # Modul for detection Operating System
import subprocess # Modul for executing the system commands


# Function for pinging a single IP address
def ping(ip_address):
    """

    Pings a given IP address to check its availability.

    Agrs:
        ip_address (str): The IP address to ping.

    Returns:
        None: Prints a message indicating whether the IP adress is available or not.

    Notes:
        - Automatically detects the operating system and adjust the ping command
        - On Linux/Unix systems, the 'ping -c 1' command send one ICMP request.
        - On Windows systems, use 'ping -n 1' instead.
    """
    
    # Determine the parameter based on the OS
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Build the ping command
    command = ['ping',param,'1',ip_address]

    try:
        #Execute the ping command and capture the output
        output = subprocess.check_output(command, universal_newlines=True)
        print(f"{ip_address} is available")
    except subprocess.CalledProcessError:
        print(f"{ip_address} is not available")

# Test function with a well-known IP address
ping("8.8.8.8") # Google DNS serverdd