# NetworkScanner

## Overview

**NetworkScanner** is a Python-based tool designed for network diagnostics and analysis. Its primary function is to check the availability of devices on a network using the ICMP protocol. The tool is ideal for basic network troubleshooting and learning how ICMP works in real-world scenarios.

## Features

- **ICMP Ping Utility**:
  - Test reachability of devices on the network.
  - Measure **latency (RTT)** and detect **packet loss**.
  - Gather additional details such as **packets transmitted**, **packets received**, and **TTL (Time To Live)**.
  - Improved execution using `subprocess` for secure and efficient command handling.
  - **User Input Support**: Allows the user to input a custom IP address or use the default value.


- **Cross-Platform Support**:
  - Compatible with Linux/Unix and Windows systems.
  - Automatically adjusts the `ping` command parameters based on the operating system.


- **Detailed Output**:
  - Displays detailed statistics for each ping, including transmitted and received packets, RTT, and TTL.
  - Detects and reports when TTL expires in transit.

## Usage

Run the script and follow the prompts to enter:
1. The IP address you want to ping.
2. The number of packets you want to send.

### Example Commands
```bash
# Run with default values
python ping_tool.py

# Run with a custom IP address and number of packets
python ping_tool.py
Enter an IP address to ping (default: 8.8.8.8): 1.1.1.1
Enter the number of packets to send (default: 1): 4
