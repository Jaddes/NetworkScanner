import tkinter as tk
from tkinter import ttk
from single import  ping # Importing function from single.py
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcyberpunk

def format_ping_result(result):
    """
    Format parsed ping output for better display in GUI
    """
    if "error" in result:
        return f"{result['error']}"

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

def update_text_widget_size(text_widget):
    """
    Dynamically adjusts the height of the Text widget based on the content.
    """
    text_widget.update_idletasks()  # Ensure latest geometry is calculated
    lines = int(text_widget.index("end-1c").split(".")[0])  # Count lines of text
    text_widget.config(height=lines + 1)  # Adjust height (+1 for padding)


def execute_ping():
    global rtt_values, packet_loss
    ip_address = ip_entry.get().strip()
    packet_count = packet_count_combobox.get().strip()

    if not ip_address:
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Error: you have not entered an IP address")
        result_text.config(state="disabled")
        update_text_widget_size(result_text)
        return

    if not packet_count.isdigit():
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Error: Invalid packet count")
        result_text.config(state="disabled")
        update_text_widget_size(result_text)
        return 

    packet_count = int(packet_count)
    result = ping(ip_address, count=packet_count)

    result_text.config(state="normal")
    result_text.delete(1.0, tk.END)
    if result:
        result_text.insert(tk.END, format_ping_result(result))
    else:
        result_text.insert(tk.END, "Error: No response from ping function.")
    result_text.config(state="disabled")  # Disable editing
    update_text_widget_size(result_text)

    # Reset RTT vrednosti i Packet Loss pre osvežavanja grafikona
    if "error" in result or not result.get('rtt_all'):
        rtt_values = []  # Postavljamo prazan RTT niz
        packet_loss = 100  # Postavljamo packet loss na 100% jer ping nije uspeo
    else:
        rtt_values = [float(rtt.replace(" ms", "")) for rtt in result.get('rtt_all', [])]
        packet_loss = int(result.get("packet_loss", "0").replace("%", ""))

    print(f"Updated RTT values: {rtt_values}")  # Debug print
    print(f"Updated Packet Loss: {packet_loss}%")  # Debug print

    # Ažuriranje grafova sa novim podacima
    show_rtt_graph(rtt_values)
    show_packet_loss_graph(packet_loss)
    

    
def show_rtt_graph(rtt_values):
    """
    Generates RTT graph and embeds it into Tkinter GUI.
    """
    # Clear previous graphs
    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 3))
    plt.style.use("cyberpunk")
    ax.plot(range(1, len(rtt_values) + 1), rtt_values, marker='o', linestyle='-', color='cyan')
    ax.set_title("RTT per Packet", color="white")
    ax.set_xlabel("Packet Number", color="white")
    ax.set_ylabel("RTT (ms)", color="white")
    ax.grid(True, color="#444444")
    fig.patch.set_facecolor('#1e1e2f')
    ax.set_facecolor("#1e1e2f")

    # Ensure axis labels are not cut off
    plt.tight_layout()  # Adjust layout to fit everything

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def show_packet_loss_graph(packet_loss):
    """
    Generates a horizontal Packet Loss graph and embeds it into Tkinter GUI.
    """
    # Clear previous graphs
    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 1.5)) 
    plt.style.use("cyberpunk")

    # Horisontal track for Packet Loss
    bars = ax.barh(["Packet Loss"], [packet_loss], color='red', height=0.4, align='center')

    ax.set_title("Packet Loss Percentage", color="white", pad=10)
    ax.set_xlabel("Loss (%)", color="white")  
    ax.set_xlim(0, 100)  
    ax.set_facecolor("#1e1e2f")
    fig.patch.set_facecolor('#1e1e2f')

    # Centralisation the label on the Y axis
    ax.set_yticks([0])  # Samo jedan label na y-osi
    ax.set_yticklabels(["Packet Loss"], ha="center", va="center", color="white")

    # Centralisation values on the bar, dynamically shifting based on the width of the bar
    for bar in bars:
        bar_width = bar.get_width()
        text_x = bar_width + 5 if bar_width < 10 else bar_width / 2  # Ako je mali gubitak, pomeri desno
        text_color = "white" if bar_width > 50 else "black"  # Kontrast teksta na crvenom baru

        ax.text(text_x, bar.get_y() + bar.get_height() / 2,
                f"{packet_loss}%", ha='center', va='center', color=text_color, fontsize=10, fontweight='bold')

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()



# Creating the main windows
root = tk.Tk()
root.title("Network Scanner - Single IP")
root.configure(bg='#1e1e2f')  # Set dark blue background

rtt_values = []
packet_loss = 0

# Styling using ttk.Style
style = ttk.Style()
style.theme_use("clam")  # Use 'clam' theme for better customization

# General styles
style.configure("TLabel", background="#1e1e2f", foreground="#d9d9d9", font=("Arial", 10, "bold"))
style.configure("TButton", background="#33334d", foreground="white", font=("Arial", 10))
style.configure("TFrame", background="#1e1e2f")
style.configure("TEntry", fieldbackground="#33334d", foreground="white", background="#33334d", font=("Arial", 10))
style.configure("TCombobox", fieldbackground="#33334d", foreground="white", background="#33334d", arrowcolor="white", font=("Arial", 10))


# Main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Left frame (Options)
left_frame = ttk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="ns")

# Right frame (Graphs and buttons)
right_frame = ttk.Frame(main_frame)
right_frame.grid(row=0, column=1, sticky="nsew")
main_frame.columnconfigure(1, weight=1)

# Configure column weight for resizing
main_frame.columnconfigure(1, weight=1)

# Input frame in left panel
ttk.Label(left_frame, text="IP Address:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ip_entry = ttk.Entry(left_frame, width=25)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(left_frame, text="Packets:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
packet_options = [str(i) for i in range(1, 100)]
packet_count_combobox = ttk.Combobox(left_frame, values=packet_options, width=5)
packet_count_combobox.set("4")
packet_count_combobox.grid(row=1, column=1, padx=5, pady=5)

ping_button = ttk.Button(left_frame, text="Ping", command=execute_ping)
ping_button.grid(row=2, column=0, columnspan=2, pady=10)

# Result text area
result_text = tk.Text(left_frame, width=40, height=15, bg="#33334d", fg="#d9d9d9", insertbackground="white")
result_text.grid(row=3, column=0, columnspan=2, pady=10)
result_text.config(state="disabled")

# Graph button frame in right panel
graph_button_frame = ttk.Frame(right_frame)
graph_button_frame.pack(pady=10)

rtt_button = ttk.Button(graph_button_frame, text="RTT per Packet", command=lambda: show_rtt_graph(rtt_values))
rtt_button.grid(row=0, column=0, padx=5)

packet_loss_button = ttk.Button(graph_button_frame, text="Packet Loss Percentage", command=lambda: show_packet_loss_graph(packet_loss))
packet_loss_button.grid(row=0, column=1, padx=5)


# Graph frame
graph_frame = ttk.Frame(right_frame)
graph_frame.pack(fill="both", expand=True)

root.mainloop()
