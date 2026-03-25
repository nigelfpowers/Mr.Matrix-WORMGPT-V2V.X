try:
    import tkinter as tk
except ImportError as error:
    tk = None
    TKINTER_IMPORT_ERROR = error
else:
    TKINTER_IMPORT_ERROR = None

try:
    import pyshark
except ImportError as error:
    pyshark = None
    PYSHARK_IMPORT_ERROR = error
else:
    PYSHARK_IMPORT_ERROR = None


class PacketAnalyzer(tk.Tk if tk is not None else object):
    def __init__(self):
        if tk is None:
            raise RuntimeError(
                "tkinter is required to run PacketAnalyzer. "
                "Install the Python tkinter package for your platform."
            ) from TKINTER_IMPORT_ERROR

        super().__init__()

        self.title("Simple Wireshark-like Tool")
        self.geometry("600x400")

        # Text widget for displaying packet info
        self.text_area = tk.Text(self, height=20, width=80)
        self.text_area.pack(pady=20)

        # Button to start packet capture
        self.start_button = tk.Button(self, text="Start Capture", command=self.start_capture)
        self.start_button.pack(pady=10)

    def start_capture(self):
        if pyshark is None:
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(
                tk.END,
                "pyshark is required to start packet capture. "
                "Install it with: pip install pyshark\n",
            )
            return

        # Setting up the capture
        self.capture = pyshark.LiveCapture(interface='your_interface_here')
        self.capture.sniff(timeout=10)
        self.display_packets()

    def display_packets(self):
        # Clear the text area before displaying new packets
        self.text_area.delete('1.0', tk.END)

        for packet in self.capture.sniff_continuously(packet_count=5):
            try:
                # Display basic packet info; customize as needed
                packet_info = f"Packet {packet.number}: {packet.highest_layer} - {packet.length} bytes\n"
                if hasattr(packet, 'ip'):
                    packet_info += f"Source IP: {packet.ip.src} -> Destination IP: {packet.ip.dst}\n"
                self.text_area.insert(tk.END, packet_info)
            except AttributeError:
                continue

def main():
    try:
        app = PacketAnalyzer()
    except RuntimeError as error:
        raise SystemExit(error) from error

    app.mainloop()


if __name__ == "__main__":
    main()
