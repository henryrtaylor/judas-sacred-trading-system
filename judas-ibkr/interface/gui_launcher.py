import tkinter as tk
from tkinter import ttk
import datetime

class JudasGUI:
    def __init__(self, root):
        self.root = root
        root.title("Judas Sacred Interface")
        root.geometry("600x400")
        self.label = tk.Label(root, text="📈 Judas Sacred System Online", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.agent_status = tk.Text(root, height=10, width=70)
        self.agent_status.pack(pady=10)

        self.log_button = tk.Button(root, text="Refresh Agent Status", command=self.load_status)
        self.log_button.pack()

    def load_status(self):
        try:
            with open("logs/trade_log.txt", "r") as f:
                lines = f.readlines()[-5:]
                self.agent_status.delete('1.0', tk.END)
                for line in lines:
                    self.agent_status.insert(tk.END, line)
        except FileNotFoundError:
            self.agent_status.insert(tk.END, "No trade logs found.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = JudasGUI(root)
    root.mainloop()
