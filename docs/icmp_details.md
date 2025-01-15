# Network Protocols

## ICMP Protocol

### Overview

The **Internet Control Message Protocol (ICMP)** is a fundamental protocol in the Internet Protocol Suite. It operates at the network layer and is used primarily for sending diagnostic information and error messages between devices.

### Use Cases

1. **Diagnostics**:
   - `Ping`: Check the availability and responsiveness of a device on the network.
   - `Traceroute`: Trace the path packets take through a network.

2. **Error Notifications**:
   - **Destination Unreachable**: Alerts when a packet cannot reach its intended destination.
   - **Time Exceeded**: Indicates that a packet's TTL (Time-To-Live) expired before reaching the destination.

### How Ping Works

1. A **client** sends an **ICMP Echo Request** (Type 8, Code 0) to the target device.
2. The **target device**, if reachable, replies with an **ICMP Echo Reply** (Type 0, Code 0).
3. The client measures:
   - **Latency (RTT)**: The round-trip time for the packet to travel to the target and back.
   - **Packet Loss**: The percentage of requests that fail to receive replies.

### ICMP Packet Structure

| Field           | Description                                                 |
|------------------|-------------------------------------------------------------|
| **Type**         | Identifies the type of ICMP message (e.g., Echo Request = 8).|
| **Code**         | Provides additional context for the Type field.             |
| **Checksum**     | Validates the integrity of the ICMP message.                |
| **Identifier**   | Used to match requests and replies.                         |
| **Sequence**     | Numbers packets for tracking and RTT calculations.          |
| **Data**         | Includes diagnostic information or payload data.            |

### Common ICMP Message Types

| Type | Code | Message                              | Description                     |
|------|------|--------------------------------------|---------------------------------|
| 0    | 0    | Echo Reply                          | Reply to an Echo Request.       |
| 3    | 0–15 | Destination Unreachable             | Destination cannot be reached.  |
| 8    | 0    | Echo Request                        | Requests an Echo Reply.         |
| 11   | 0    | Time Exceeded                       | TTL expired in transit.         |

## Metrics Explained

### **RTT (Round-Trip Time)**
- **What it is**: RTT measures the total time for a packet to travel from the source to the destination and back.
- **How it is calculated**:
  - Extracted from the `time=XX ms` field in the ping command output.
  - The tool calculates **Min**, **Avg**, and **Max** RTT values across multiple packets.
- **Example Output**:

### **TTL (Time-To-Live)**
- **What it is**: TTL limits the number of hops (routers) a packet can traverse before being discarded.
- **How it works in the tool**:
- Extracted from the `ttl=XX` field in the ping command output.
- Calculates how many hops the packet passed based on the initial TTL (64 for Linux/Unix, 128 for Windows).
- **Example Output**:

### Advantages of ICMP

- Simple and efficient for basic network diagnostics.
- Provides insights into network health and device availability.

### Limitations of ICMP

- Vulnerable to misuse in attacks (e.g., Ping Flood in DDoS scenarios).
- Often disabled on networks for security reasons, limiting its utility.

## Implementation Details

The tool executes the `ping` command using Python's `subprocess` module. This ensures:
- Secure execution of system commands.
- Capturing and analyzing the output of the `ping` command for better error handling.
- Automatic detection of the operating system to adjust command parameters (`-c` for Linux/Unix and `-n` for Windows).
- **User Input Feature**:
  - The tool prompts the user to enter an IP address to ping.
  - If no input is provided, the tool defaults to `8.8.8.8`.
- **Enhanced Output**:
  - Provides detailed statistics, including RTT, Packet Loss, Transmitted/Received packets, and TTL.



For more information, see the [README.md](README.md) file.
