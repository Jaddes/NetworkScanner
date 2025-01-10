import os # Importing a modul for working with systems commands

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


    # Executing the system command for ping
    response = os.system(f"ping -c 1 {ip_address}") # For Linux/Unix systems
    # response = os.system(f"ping -n 1 {ip_adress}") # For Windows systems

    # Checking if the device is available
    if response == 0:
        print(f"{ip_address} is available")
    else:
        print(f"{ip_address} is not available")

# Test function with a well-known IP address
ping("8.8.8.8") # Google DNS server