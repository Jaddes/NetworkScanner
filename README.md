# NetworkScanner

## Overview

**NetworkScanner** is a Python-based tool designed for network diagnostics and analysis. Its primary function is to check the availability of devices on a network using the ICMP protocol. The tool provides detailed statistics and supports parallel pinging for multiple IP addresses.

## Features

- **ICMP Ping Utility**:
  - Test reachability of devices on the network.
  - Measure **latency (RTT)** (Min/Avg/Max) and detect **packet loss**.
  - Gather additional details such as **packets transmitted**, **packets received**, and **TTL (Time To Live)**.
  - **Ping Multiple IPs**: Allows the user to ping multiple IP addresses entered as a comma-separated list, with parallel execution.
  - Improved execution using `subprocess` for secure and efficient command handling.
  - **User Input Support**: Enables input of a single IP address, multiple IPs, or default values.
  - **Range Ping**
    - Supports pinging multiple IP adresses within a specified range (e.g., 192.168.1.1 to 192.168.1.10)
    - Automatically generates all IP addresses in the specified range and pings them sequentially or in parallel
    - Provides detailed results for each IP in the range

- **Cross-Platform Support**:
  - Compatible with Linux/Unix and Windows systems.
  - Automatically adjusts the `ping` command parameters based on the operating system.

- **Logging Results**:
  - Saves detailed results for each ping (including errors) to a log file with timestamps.**

- **Detailed Output**:
  - Displays comprehensive statistics for each ping, including:
    - RTT (Min/Avg/Max).
    - Packet Loss.
    - Packets Transmitted/Received.
    - TTL and hop count.

## Usage

Run the script and follow the prompts to:
1. Enter a single IP address or multiple IP addresses (comma-separated).
2. Specify the number of packets you want to send.

### Example Commands
```bash
# Run with default values
python ping_tool.py

# Run with a single custom IP address and number of packets
python ping_tool.py
Enter an IP address to ping (default: 8.8.8.8): 1.1.1.1
Enter the number of packets to send (default: 1): 4

# Run with multiple IP addresses
python ping_tool.py
Enter IP addresses to ping (comma-separated, default: 8.8.8.8): 8.8.8.8,1.1.1.1
Enter the number of packets to send (default: 1): 2
**