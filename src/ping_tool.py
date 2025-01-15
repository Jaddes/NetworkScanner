import platform # Modul for detection Operating System
import subprocess # Modul for executing the system commands
from parse_ping_tool import parse_ping_output # Implementing function for parsing

# Function for pinging a single IP address
def ping(ip_address, count):
    """

    Pings a given IP address to check its availability and extracts detailed information.

    Agrs:
        ip_address (str): The IP address to ping.

    Returns:
        None: Prints detailed information about the ping request.

    Notes:
        - Automatically detects the operating system and adjust the ping command
        - On Linux/Unix systems, the 'ping -c <count>' command send one ICMP request.
        - On Windows systems, use 'ping -n <count>' instead.
    """
    
    # Determine the parameter based on the OS
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Build the ping command
    command = ['ping',param,str(count),ip_address]

    try:
        #Execute the ping command and capture the output
        output = subprocess.check_output(command, universal_newlines=True)

        # Parse the output for useful information
        stats = parse_ping_output(output)

        print(f"\nPing Results for {ip_address}:")
        print(f"  - RTT (Min/Avg/Max): {stats.get('rtt_min', 'N/A')} / {stats.get('rtt_avg', 'N/A')} / {stats.get('rtt_max', 'N/A')}")
        print(f"  - RTT Values (All): {', '.join(stats.get('rtt_all', []))}")
        print(f"  - Packet Loss: {stats.get('packet_loss', 'N/A')}")
        print(f"  - Packets Transmitted: {stats.get('packets_transmitted', 'N/A')}")
        print(f"  - Packets Received: {stats.get('packets_received', 'N/A')}")
        print(f"  - TTL (Final): {stats.get('ttl_final', 'N/A')}")
        print(f"  - Additional TTL Info: {stats.get('ttl_info', 'None')}")

    except subprocess.CalledProcessError as e:
        print(f"{ip_address} is not available")
        print(f"Error: {e.output}")            

if __name__ == "__main__":
    # Prompt the user for an IP address
    user_input = input("Enter an IP address to ping (default: 8.8.8.8): ").strip()
    ip_address = user_input if user_input else "8.8.8.8"

    # Prompt the user for number of packets
    user_input_count = input("Enter the number of packets to send (default: 1): ").strip()
    count = int(user_input_count) if user_input_count.isdigit() else 1   

    # Test function with a well-known IP address
    ping(ip_address, count) # Google DNS serverdd