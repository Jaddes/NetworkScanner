import platform # Modul for detection Operating System
import subprocess # Modul for executing the system commands
import threading # Parallel execution module
import datetime # Module for timestamp in logs
import ipaddress # Module for generating IP address ranges
from tabulate import tabulate
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

        # print(f"\nPing Results for {ip_address}:")
        # print(f"  - RTT (Min/Avg/Max): {stats.get('rtt_min', 'N/A')} / {stats.get('rtt_avg', 'N/A')} / {stats.get('rtt_max', 'N/A')}")
        # print(f"  - RTT Values (All): {', '.join(stats.get('rtt_all', []))}")
        # print(f"  - Packet Loss: {stats.get('packet_loss', 'N/A')}")
        # print(f"  - Packets Transmitted: {stats.get('packets_transmitted', 'N/A')}")
        # print(f"  - Packets Received: {stats.get('packets_received', 'N/A')}")
        # print(f"  - TTL (Final): {stats.get('ttl_final', 'N/A')}")
        # print(f"  - Additional TTL Info: {stats.get('ttl_info', 'None')}")

        return stats
    except subprocess.CalledProcessError as e:
        return {"ip": ip_address, "error": e.output}

def ping_multiple_ips_parallel(ip_list, count=1):
    """
    Pings multiple IP addresses in parallel and logs results.

    Args:
        ip_list (list): List of IP addresses to ping.
        count (int): Number of packets to send for each address.

    Returns:
        None
    """
    threads = []
    results = []

    def ping_and_log(ip):
        # Check the validity of the IP address
        ip = str(ip.strip())
        try:
            stats = ping(ip, count)
            if stats is None:
                stats = {"ip": ip, "error": "Ping command failed"}
        except Exception as e:
            stats = {"ip": ip, "error": str(e)}
        stats["ip"] = ip
        log_results(ip, stats)
        results.append(stats)

    for ip in ip_list:
        thread = threading.Thread(target=ping_and_log, args=(ip,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Display results in a table
    display_results_in_table(results)


def log_results(ip_address, stats, filename="ping_results.log"):
    """
    Logs the ping results to a file with a timestamp.

    Args:
        ip_address (str): The IP address that was pinged.
        stats (dict): Parsed statistics from the ping command.
        filename (str): The name of the log file (default: ping_results.log).

    Returns:
        None
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as log_file:
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"Results for {ip_address}:\n")
        if "error" in stats:
            log_file.write(f"  - Error: {stats['error']}\n")
        else:
            for key, value in stats.items():
                log_file.write(f"  - {key}: {value}\n")
        log_file.write("\n")

def display_results_in_table(results):
    headers = ["IP Address", "RTT (Min/Avg/Max)", "Packet Loss", "TTL"]
    table = []
    for res in results:
        table.append([
            res.get("ip", "Unknown"),
            f"{res.get('rtt_min', 'N/A')} / {res.get('rtt_avg', 'N/A')} / {res.get('rtt_max', 'N/A')}",
            res.get("packet_loss", "N/A"),
            res.get("ttl_final", "N/A")
        ])
    
    if table:
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("No results to display.")



def generate_ip_range(start_ip, end_ip):
    """
    Generates a list of individual IP addresses within a given range.

    Args:
        start_ip (str): The starting IP address.
        end_ip (str): The ending IP address.

    Returns:
        list: A list of IP addresses within the range.
    """
    try:
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        if start > end:
            raise ValueError("Start IP must be less than or equal to End IP")
        return [str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)]
    except ValueError as e:
        print(f"Invalid IP range: {e}")
        return []


if __name__ == "__main__":
    # User input for pinging range or multiple IPs
    mode = input("Enter mode (single, multiple, range): ").strip().lower()

    if mode == "range":
        start_ip = input("Enter the starting IP address: ").strip()
        end_ip = input("Enter the ending IP address: ").strip()
        ip_list = generate_ip_range(start_ip, end_ip)
    elif mode == "multiple":
        user_input_ips = input("Enter IP addresses to ping (comma-separated): ").strip()
        ip_list = user_input_ips.split(',')
    else:  # Default to single IP
        ip_list = [input("Enter an IP address to ping (default: 8.8.8.8): ").strip() or "8.8.8.8"]

    user_input_count = input("Enter the number of packets to send (default: 1): ").strip()
    count = int(user_input_count) if user_input_count.isdigit() else 1

    ping_multiple_ips_parallel(ip_list, count)