import subprocess
import platform
import re

def ping(ip_address, count=1):
    """

    Function for pinging one IP address

    """
    

    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), ip_address]

    try:
        output = subprocess.check_output(command, universal_newlines=True)
        stats = parse(output)
        stats["ip"] = ip_address
        return stats
        
    except subprocess.CalledProcessError as e:
        print(f"Ping was not successful for {ip_address}: {e.output}")  # Debug
        return {"error": f"Host {ip_address} is unreachable", "packet_loss": "100%"} 

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

        # Calculating  jitter (difference between adjacent RTT values)
        if len(rtt_values) > 1:
            jitter_values = [abs(rtt_values[i] - rtt_values[i - 1]) for i in range(1, len(rtt_values))]
            result['jitter'] = f"{sum(jitter_values) / len(jitter_values):.2f} ms"
        else:
            result['jitter'] = "N/A"
    else:
        result['rtt_all'] = []
        result['rtt_min'] = "N/A"
        result['rtt_avg'] = "N/A"
        result['rtt_max'] = "N/A"

    # Parse for packet loss
    match = re.search(r'(\d+)% packet loss', output)
    if match:
        result['packet_loss'] = f"{match.group(1)}%"
    else:
        result['packet_loss'] = "100%"  # Ako ping ne uspe, smatraj da je gubitak paketa 100%

    # Parse for TTL  
    ttl_match = re.search(r'TTL=(\d+)', output, re.IGNORECASE)
    if ttl_match:
        result['ttl'] = ttl_match.group(1)
    else:
        result['ttl'] = "N/A"

    return result



    
        


    

