import platform # Modul for detection Operating System
import subprocess # Modul for executing the system commands
import threading # Parallel execution module
import datetime 
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

        print(f"\nPing Results for {ip_address}:")
        print(f"  - RTT (Min/Avg/Max): {stats.get('rtt_min', 'N/A')} / {stats.get('rtt_avg', 'N/A')} / {stats.get('rtt_max', 'N/A')}")
        print(f"  - RTT Values (All): {', '.join(stats.get('rtt_all', []))}")
        print(f"  - Packet Loss: {stats.get('packet_loss', 'N/A')}")
        print(f"  - Packets Transmitted: {stats.get('packets_transmitted', 'N/A')}")
        print(f"  - Packets Received: {stats.get('packets_received', 'N/A')}")
        print(f"  - TTL (Final): {stats.get('ttl_final', 'N/A')}")
        print(f"  - Additional TTL Info: {stats.get('ttl_info', 'None')}")

        return stats
    except subprocess.CalledProcessError as e:
        print(f"{ip_address} is not available")
        print(f"Error: {e.output}")

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
        stats = ping(ip.strip(), count)
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
    """
    Displays ping results in a table format.

    Args:
        results (list): List of dictionaries containing ping results.

    Returns:
        None
    """
    headers = ["IP Address", "RTT (Min/Avg/Max)", "Packet Loss", "TTL"]
    table = []
    for res in results:
        if "error" in res:
            table.append([res["ip"], "N/A", "N/A", "N/A"])
        else:
            table.append([
                res["ip"],
                f"{res['rtt_min']} / {res['rtt_avg']} / {res['rtt_max']}",
                res["packet_loss"],
                res["ttl_final"]
            ])
    print(tabulate(table, headers=headers, tablefmt="grid"))

    

if __name__ == "__main__":
    # User input for IP addresses
    user_input_ips = input("Enter IP addresses to ping (comma-separated, default: 8.8.8.8): ").strip()
    ip_addresses = user_input_ips.split(',') if user_input_ips else ["8.8.8.8"]

    # User input for number of packets
    user_input_count = input("Enter the number of packets to send (default: 1): ").strip()
    count = int(user_input_count) if user_input_count.isdigit() else 1  

    # Ping one or multiple IP addresses
    ping_multiple_ips_parallel(ip_addresses, count)