import tkinter as tk
from tkinter import ttk
from single import  ping # Importing function from single.py
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def format_ping_result(result):
    """
    Format parsed ping output for better display in GUI
    """
    if "error" in result:
        return f"❌ {result['error']}"

    formatted_result = f"""
    Result for {result.get('ip', 'Unknown')}:
    --------------------------------
    RTT Min:      {result.get('rtt_min', 'N/A')}
    RTT Avg:      {result.get('rtt_avg', 'N/A')}
    RTT Max:      {result.get('rtt_max', 'N/A')}
    Packet Loss:  {result.get('packet_loss', 'N/A')}
    --------------------------------
    """
    return formatted_result

def execute_ping():
    ip_address = ip_entry.get().strip() # Taking the ip address from the input field
    packet_count = packet_count_combobox.get().strip()

    if not ip_address: # Check if it is empty or not
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Error: you have not entered an IP address")
        return

    if not packet_count.isdigit():
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Error: Invalid packet count")
        return 

    packet_count = int(packet_count)   

    result = ping(ip_address) # Call ping function

    result_text.delete(1.0, tk.END) # Cleaing the previous results
    if result:
        result_text.insert(tk.END,format_ping_result(result)) # Display of results
    else:
        result_text.insert(tk.END, "Error: No response from ping function.")

    # Extract RTT values & packet loss
    if "error" not in result:
        rtt_values = [float(rtt.replace(" ms", "")) for rtt in result.get('rtt_all', [])]
        packet_loss = int(result.get("packet_loss", "%0").replace("%", ""))

        # Call the function to plot graphs
        plot_graphs(rtt_values, packet_loss)

def plot_graphs(rtt_values, packet_loss):
    """
    Generates RTT and Packet Loss graphs and embeds them into Tkinter GUI.
    """
    # Clear previous graphs
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Create Matplotlib Figure
    fig, axs = plt.subplots(2, 2, figsize=(5, 5))  # Two graphs stacked vertically

    # 1️⃣ RTT Graph (Line Chart)
    axs[0].plot(range(1, len(rtt_values) + 1), rtt_values, marker='o', linestyle='-', color='blue')
    axs[0].set_title("RTT per Packet")
    axs[0].set_xlabel("Packet Number")
    axs[0].set_ylabel("RTT (ms)")
    axs[0].grid(True)

    # 2️⃣ Packet Loss Graph (Bar Chart)
    axs[1].bar(["Packet Loss"], [packet_loss], color='red')
    axs[1].set_ylim(0, 100)  # Scale 0-100%
    axs[1].set_title("Packet Loss Percentage")
    axs[1].set_ylabel("Loss (%)")

    # Embed the Figure in Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    

# Creating the main windows
root = tk.Tk()
root.title("Network Scanner - Single IP")

# Frame for IP input + packet count
input_frame = ttk.Frame(root)
input_frame.pack(pady=5)

# Label and Entry for IP address
ttk.Label(input_frame, text="IP Address:").grid(row=0, column=0, padx=5)
ip_entry = ttk.Entry(input_frame, width=25)
ip_entry.grid(row=0, column=1, padx=5)

# Input Filed for number of packets
ttk.Label(input_frame, text="Packets:").grid(row=0, column=2, padx=5)
packet_options = [str(i) for i in range(1,100)] # List of values from 1 to 100
packet_count_combobox = ttk.Combobox(input_frame, values=packet_options, width=5)
packet_count_combobox.set("4") # Default value
packet_count_combobox.grid(row=0, column=3, padx=5)

# Button for running the ping
ping_button = ttk.Button(root, text="Ping", command=execute_ping)
ping_button.pack(pady=30)

# Text Field for the result
result_text = tk.Text(root, width = 60, height=15)
result_text.pack(pady=10)

# Frame for graphs
graph_frame = ttk.Frame(root)
graph_frame.pack(pady=10)

# Pokretanje glavne petlje
root.mainloop()
