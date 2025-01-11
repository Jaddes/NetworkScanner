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


- **Customizable**:
  - Easily extend the functionality to include other network protocols and features.

## Usage

Run the script and follow the prompt to enter an IP address. If no address is provided, the tool will default to `8.8.8.8`:

```bash
python ping_tool.py

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- Basic knowledge of how to use the command line.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jaddes/NetworkScanner.git
