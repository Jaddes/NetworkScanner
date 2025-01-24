import re 
import platform

def parse_ping_output(output):
    """

    Parses the output of the ping command to extract detailed information.

    Args:
        output (str): The raw output of the ping command.

    Returns:
        dict: A dictionary containing RTT, packet loss, and other details.

    """
    result = {}

    # Check the output
    if not output.strip():
        return {"error": "No output from ping command"}

    # Parse RTT for each packet
    rtt_values = re.findall(r'time=(\d+\.?\d*) ms', output)
    if rtt_values:
        rtt_values = [float(rtt) for rtt in rtt_values if float(rtt) > 0]  # Fillter the null values
        if rtt_values:
            result['rtt_min'] = f"{min(rtt_values):.2f} ms"
            result['rtt_avg'] = f"{sum(rtt_values)/len(rtt_values):.2f} ms"
            result['rtt_max'] = f"{max(rtt_values):.2f} ms"
            result['rtt_all'] = [f"{rtt:.2f} ms" for rtt in rtt_values]
    # Parse packet loss
    match = re.search(r'(\d+)% packet loss', output)
    if match:
        result['packet_loss'] = f"{match.group(1)}%"

    # Parse transmitted and received packets
    match = re.search(r'(\d+) packets transmitted, (\d+) received', output)
    if match:
        result['packets_transmitted'] = match.group(1)
        result['packets_received'] = match.group(2)

    # Parse TTL (for last packet)
    match = re.search(r'ttl=(\d+)', output, re.IGNORECASE)
    if match:
        ttl_final = int(match.group(1))  # Final TTL value
        result['ttl_final'] = ttl_final


        # Determine initial TTL based on OS
        if platform.system().lower() == 'windows':
            initial_ttl = 128
        else:
            initial_ttl = 64

        # Calculate hops passed        
        hops_passed = initial_ttl - ttl_final

        if hops_passed > 0:
            result['ttl_info'] = f"TTL indicates {hops_passed} hops passed"
        else:
            result['ttl_info'] = "Reached destination successfully"

    # Parse TTL expiration messages
    match = re.search(r'TTL expired in transit|Time to live exceeded', output, re.IGNORECASE)
    if match:
        result['ttl_info'] = "TTL expired during transmission"

    return result