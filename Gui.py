import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SalesForecastApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Forecasting App")
        self.root.geometry("1000x700")
        self.data = None
        self.canvas = None

        self.setup_widgets()

    def setup_widgets(self):
        # Top frame for buttons
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Upload CSV
        self.upload_button = tk.Button(top_frame, text="Upload CSV", command=self.upload_csv)
        self.upload_button.pack(side=tk.LEFT, padx=5)

        # Clear data
        self.clear_button = tk.Button(top_frame, text="Clear", command=self.clear_data)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Forecast
        self.forecast_button = tk.Button(top_frame, text="Train and Forecast", command=self.train_and_forecast)
        self.forecast_button.pack(side=tk.LEFT, padx=5)

        # Export
        self.export_button = tk.Button(top_frame, text="Export Forecast", command=self.export_forecast)
        self.export_button.pack(side=tk.LEFT, padx=5)

        # Filename label
        self.filename_label = tk.Label(top_frame, text="No file selected", fg="gray")
        self.filename_label.pack(side=tk.LEFT, padx=10)

        # Middle frame for data preview
        mid_frame = tk.Frame(self.root)
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview with scrollbars
        self.tree_scroll_y = tk.Scrollbar(mid_frame)
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_scroll_x = tk.Scrollbar(mid_frame, orient='horizontal')
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree = ttk.Treeview(mid_frame, yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        # Bottom frame for forecast plot
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Status bar
        self.status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            self.data = pd.read_csv(file_path)
            self.filename_label.config(text=f"Loaded: {file_path.split('/')[-1]}")
            self.status.config(text="CSV Loaded Successfully")
            self.preview_csv()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV:\n{e}")
            self.status.config(text="Error loading file")

    def preview_csv(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.data.columns)
        self.tree["show"] = "headings"

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        for _, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def clear_data(self):
        self.data = None
        self.tree.delete(*self.tree.get_children())
        self.filename_label.config(text="No file selected")
        self.status.config(text="Cleared data")
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    def train_and_forecast(self):
        if self.data is None or 'Date' not in self.data.columns or 'Sales' not in self.data.columns:
            messagebox.showerror("Error", "CSV must contain 'Date' and 'Sales' columns")
            return

        # Simulate forecast plot
        self.status.config(text="Forecasting... (mock data)")
        self.plot_forecast()

    def plot_forecast(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(self.data['Sales'], label="Actual Sales")
        ax.plot([None]*(len(self.data)-1) + [self.data['Sales'].iloc[-1]+10], linestyle='--', label="Forecast")
        ax.set_title("Sales Forecast (Sample)")
        ax.legend()
        ax.set_xlabel("Index")
        ax.set_ylabel("Sales")

        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def export_forecast(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please load and forecast data first.")
            return
        try:
            self.data.to_csv("forecast_output.csv", index=False)
            messagebox.showinfo("Exported", "Forecast exported to forecast_output.csv")
            self.status.config(text="Forecast exported successfully")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
            self.status.config(text="Failed to export forecast")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesForecastApp(root)
    root.mainloop()
