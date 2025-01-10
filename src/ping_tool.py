import platform
import subprocess


# Function for pinging a single IP address
def ping(ip_address):
    """

    Pings a given IP address to check its availability.

    Agrs:
        ip_address (str): The IP address to ping.

    Returns:
        None: Prints a message indicating whether the IP adress is available or not.

    Notes:
        - On Linux/Unix systems, the 'ping -c 1' command send one ICMP request.
        - On Windows systems, use 'ping -n 1' instead.
    """
    
    # Determine the parameter based on the OS
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Build the ping command
    command = ['ping',param,'1',ip_address]

    try:
        #Execute the ping command
        output = subprocess.check_output(command, universal_newlines=True)
        print(f"{ip_address} is available")
    except subprocess.CalledProcessError:
        print(f"{ip_address} is not available")

# Test function with a well-known IP address
ping("8.8.8.8") # Google DNS serverdd