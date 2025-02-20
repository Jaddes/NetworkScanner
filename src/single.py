import subprocess
import platform
import re

def ping(ip_address, count=1):
    """

    Function for pinging one IP address

    """
    
    # Determing which OS is user using
    # if '-n' then its a windows if not its linux so we use '-c'
    # original command is supposed to go "ping -n/-c 1(number of packets) 8.8.8.8(the address)"
    print(f"Received count in ping function: {count}")  # Debug
    param = '-n' if platform.system().lower() == 'windows' else '-c'


    # We are combining all the parts of the command into one array
    # 'ping -c 1 8.8.8.8 example
    command = ['ping', param, str(count), ip_address]
    print(f"Command executed: {' '.join(command)}") # Debug Print Ping command

    try:
        # We are executing the ping command and gonna capture the output
        output = subprocess.check_output(command, universal_newlines=True)
        print(f"Ping output:\n{output}")  # Debug for the final destination of number of packets

        # print(output) # Test the ou
        stats = parse(output)
        stats["ip"] = ip_address
        return stats
        
    except subprocess.CalledProcessError as e:
        print(f"Ping was not successful for {ip_address}: {e.output}")

def parse(output):
    """

    Parse the output of the ping command to extract detailed information

    """

    result = {}

    # Check if the output is empty
    if not output.strip():
        return{"error": "No output from ping command"}

    # Parse RTT for each packet
    rtt_values = re.findall(r'time=(\d+\.?\d*) ms', output)
    if rtt_values:
        rtt_values = [float(rtt) for rtt in rtt_values] # Converting to string
        print(f"Extracted RTT values: {rtt_values}") # Debug: Print RTT values
        result['rtt_min'] = f"{min(rtt_values):.2f} ms" if rtt_values else "N/A"
        result['rtt_avg'] = f"{sum(rtt_values)/len(rtt_values):.2f} ms"
        result['rtt_max'] = f"{max(rtt_values):.2f} ms"
        result['rtt_all'] = [f"{rtt:.2f} ms" for rtt in rtt_values]

    else:
        result['rtt_all'] = []
        result['rtt_min'] = "N/A"
        result['rtt_avg'] = "N/A"
        result['rtt_max'] = "N/A"

    # Parse for packet loss
    match = re.search(r'(\d+)% packet loss', output)
    result['packet_loss'] = f"{match.group(1)}%"

    return result



    
        


    

