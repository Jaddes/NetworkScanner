import re 

def parse_ping_output(output):
    """

    Parses the output of the ping command to extract detailed information.

    Args:
        output (str): The raw output of the ping command.

    Returns:
        dict: A dictionary containing RTT, packet loss, and other details.

    """
    result = {}

    # Parse RTT
    match = re.search(r'time=(\d+\.?\d*) ms', output)
    if match:
        result['rtt'] = f"{match.group(1)} ms"

    # Parse packet loss
    match = re.search(r'(\d+)% packet loss', output)
    if match:
        result['packet_loss'] = f"{match.group(1)}%"

    # Parse transmitted and received packets
    match = re.search(r'(\d+) packets transmitted, (\d+) received', output)
    if match:
        result['packets_transmitted'] = match.group(1)
        result['packets_received'] = match.group(2)

    # Parse TTL (Time To Live)
    match = re.search(r'ttl=(\d+)', output, re.IGNORECASE)
    if match:
        result['ttl'] = match.group(1)

    return result