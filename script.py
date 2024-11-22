import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Scrollbar

# Set up the main Tkinter window
class CPUSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1200x800")

        # Set up main frame with two columns
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left column frame for inputs
        self.left_frame = tk.Frame(self.main_frame, bg='#D0C3C3', width=400, padx=30)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Adding a collapsible panel for inputs
        self.inputs_panel = ttk.LabelFrame(self.left_frame, text="Input Parameters", padding=(10, 10))
        self.inputs_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Dropdown for selecting scheduling algorithm
        self.algorithm_label = tk.Label(self.inputs_panel, text="Select Scheduling Algorithm:", font=('Helvetica', 18))
        self.algorithm_label.pack(anchor='w', pady=5)

        self.algorithm_var = tk.StringVar()
        self.algorithm_dropdown = ttk.Combobox(self.inputs_panel, textvariable=self.algorithm_var, state='readonly', width=35)
        self.algorithm_dropdown['values'] = ("FCFS", "SJF", "Priority", "Round Robin", "SRTF")
        self.algorithm_dropdown.current(0)
        self.algorithm_dropdown.pack(anchor='w', pady=5)

        # Input fields for number of processes, arrival time, burst time, etc.
        self.num_processes_label = tk.Label(self.inputs_panel, text="Number of Processes:")
        self.num_processes_label.pack(anchor='w', pady=5)
        self.num_processes_entry = tk.Entry(self.inputs_panel, font=('Helvetica', 18), width=35)
        self.num_processes_entry.pack(anchor='w', pady=5)

        self.arrival_times_label = tk.Label(self.inputs_panel, text="Arrival Times (comma-separated):")
        self.arrival_times_label.pack(anchor='w', pady=5)
        self.arrival_times_entry = tk.Entry(self.inputs_panel, font=('Helvetica', 18), width=35)
        self.arrival_times_entry.pack(anchor='w', pady=5)

        self.burst_times_label = tk.Label(self.inputs_panel, text="Burst Times (comma-separated):")
        self.burst_times_label.pack(anchor='w', pady=5)
        self.burst_times_entry = tk.Entry(self.inputs_panel, font=('Helvetica', 18), width=35)
        self.burst_times_entry.pack(anchor='w', pady=5)

        self.priority_label = tk.Label(self.inputs_panel, text="Priorities (comma-separated, if applicable):")
        self.priority_label.pack(anchor='w', pady=5)
        self.priority_entry = tk.Entry(self.inputs_panel, font=('Helvetica', 18), width=35)
        self.priority_entry.pack(anchor='w', pady=5)

        self.time_quantum_label = tk.Label(self.inputs_panel, text="Time Quantum (for Round Robin):")
        self.time_quantum_label.pack(anchor='w', pady=5)
        self.time_quantum_entry = tk.Entry(self.inputs_panel, font=('Helvetica', 18), width=35)
        self.time_quantum_entry.pack(anchor='w', pady=5)

        # Button to simulate scheduling
        self.simulate_button = tk.Button(self.left_frame, text="Simulate Scheduling", command=self.simulate, font=('Helvetica', 18, 'bold'))
        self.simulate_button.pack(pady=10)

        # Right column frame for outputs (larger space)
        self.right_frame = tk.Frame(self.main_frame, bg='white')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Placeholder for Gantt chart
        self.chart_frame = ttk.LabelFrame(self.right_frame, text="Gantt Chart", padding=(10, 10))
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.figure = plt.Figure(figsize=(8, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.chart_frame)
        self.canvas.get_tk_widget().pack(pady=10, anchor='center')

        # Placeholder for metrics
        self.metrics_frame = ttk.LabelFrame(self.right_frame, text="Metrics", padding=(10, 10))
        self.metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.metrics_table = ttk.Treeview(self.metrics_frame, columns=("Process", "Arrival Time", "Burst Time", "TAT", "WT"), show='headings')
        self.metrics_table.heading("Process", text="Process")
        self.metrics_table.tag_configure('center', font=('Helvetica', 16))
        self.metrics_table.heading("Arrival Time", text="Arrival Time")
        self.metrics_table.heading("Burst Time", text="Burst Time")
        self.metrics_table.heading("TAT", text="Turnaround Time (TAT)")
        self.metrics_table.heading("WT", text="Waiting Time (WT)")

        # Center-aligning the table contents
        self.metrics_table.column("Process", anchor='center')
        self.metrics_table.column("Arrival Time", anchor='center')
        self.metrics_table.column("Burst Time", anchor='center')
        self.metrics_table.column("TAT", anchor='center')
        self.metrics_table.column("WT", anchor='center')

        self.metrics_table.pack(padx=10, pady=10)

        self.metrics_scrollbar = Scrollbar(self.metrics_frame, orient="vertical", command=self.metrics_table.yview)
        if len(self.metrics_table.get_children()) > 10:
            self.metrics_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=10)
        self.metrics_table.configure(yscroll=self.metrics_scrollbar.set)
        

    def simulate(self):
        # Retrieve user input
        algorithm = self.algorithm_var.get()
        num_processes = int(self.num_processes_entry.get())
        arrival_times = list(map(int, self.arrival_times_entry.get().split(',')))
        burst_times = list(map(int, self.burst_times_entry.get().split(',')))
        priorities = list(map(int, self.priority_entry.get().split(','))) if self.priority_entry.get() else None
        time_quantum = int(self.time_quantum_entry.get()) if self.time_quantum_entry.get() else None

        # Clear previous Gantt chart and metrics
        self.ax.clear()
        for item in self.metrics_table.get_children():
            self.metrics_table.delete(item)

        # Scheduling logic based on selected algorithm
        if algorithm == "FCFS":
            start_times, end_times = self.fcfs_scheduling(num_processes, arrival_times, burst_times)
        elif algorithm == "SJF":
            start_times, end_times = self.sjf_scheduling(num_processes, arrival_times, burst_times)
        elif algorithm == "Priority":
            start_times, end_times = self.priority_scheduling(num_processes, arrival_times, burst_times, priorities)
        elif algorithm == "Round Robin":
            start_times, end_times = self.rr_scheduling(num_processes, arrival_times, burst_times, time_quantum)
        elif algorithm == "SRTF":
            start_times, end_times = self.srtf_scheduling(num_processes, arrival_times, burst_times)

        # Calculate metrics
        tat = [end_times[i] - arrival_times[i] for i in range(num_processes)]
        wt = [tat[i] - burst_times[i] for i in range(num_processes)]
        avg_tat = sum(tat) / num_processes
        avg_wt = sum(wt) / num_processes

        # Display metrics in a table
        for i in range(num_processes):
            self.metrics_table.insert("", "end", values=(f"P{i+1}", arrival_times[i], burst_times[i], tat[i], wt[i]))

        # Append average metrics at the end of the table
        self.metrics_table.insert("", "end", values=("Average", "-", "-", f"{avg_tat:.2f}", f"{avg_wt:.2f}"))

        # Draw Gantt chart on the canvas
        self.canvas.draw()

    def fcfs_scheduling(self, num_processes, arrival_times, burst_times):
        # Sort processes by arrival time (FCFS scheduling)
        processes = list(range(num_processes))
        processes.sort(key=lambda x: arrival_times[x])

        # Calculate start and end times for each process
        start_times = [0] * num_processes
        end_times = [0] * num_processes
        current_time = 0

        for i in processes:
            if current_time < arrival_times[i]:
                current_time = arrival_times[i]
            start_times[i] = current_time
            end_times[i] = current_time + burst_times[i]
            current_time = end_times[i]

        # Plot Gantt chart
        for i in processes:
            self.ax.barh(f"P{i+1}", burst_times[i], left=start_times[i], color='skyblue')
        self.ax.set_title("Gantt Chart - FCFS Scheduling")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Process")

        return start_times, end_times

    def sjf_scheduling(self, num_processes, arrival_times, burst_times):
        # Sort processes by burst time, breaking ties with arrival time
        processes = list(range(num_processes))
        processes.sort(key=lambda x: (arrival_times[x], burst_times[x]))

        # Calculate start and end times for each process
        start_times = [0] * num_processes
        end_times = [0] * num_processes
        current_time = 0

        for i in processes:
            if current_time < arrival_times[i]:
                current_time = arrival_times[i]
            start_times[i] = current_time
            end_times[i] = current_time + burst_times[i]
            current_time = end_times[i]

        # Plot Gantt chart
        for i in processes:
            self.ax.barh(f"P{i+1}", burst_times[i], left=start_times[i], color='lightgreen')
        self.ax.set_title("Gantt Chart - SJF Scheduling")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Process")

        return start_times, end_times

    def priority_scheduling(self, num_processes, arrival_times, burst_times, priorities):
        # Sort processes by priority, breaking ties with arrival time
        processes = list(range(num_processes))
        processes.sort(key=lambda x: (priorities[x], arrival_times[x]))

        # Calculate start and end times for each process
        start_times = [0] * num_processes
        end_times = [0] * num_processes
        current_time = 0

        for i in processes:
            if current_time < arrival_times[i]:
                current_time = arrival_times[i]
            start_times[i] = current_time
            end_times[i] = current_time + burst_times[i]
            current_time = end_times[i]

        # Plot Gantt chart
        for i in processes:
            self.ax.barh(f"P{i+1}", burst_times[i], left=start_times[i], color='orange')
        self.ax.set_title("Gantt Chart - Priority Scheduling")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Process")

        return start_times, end_times

    def rr_scheduling(self, num_processes, arrival_times, burst_times, time_quantum):
        # Round Robin scheduling logic
        remaining_burst_times = burst_times[:]
        current_time = 0
        completed = 0
        n = len(arrival_times)
        process_queue = []
        gantt_chart = []
        start_times = [-1] * num_processes
        end_times = [0] * num_processes

        while completed < n:
            # Add processes that have arrived
            for i in range(num_processes):
                if arrival_times[i] <= current_time and i not in process_queue and remaining_burst_times[i] > 0:
                    process_queue.append(i)
            if process_queue:
                i = process_queue.pop(0)
                if start_times[i] == -1:
                    start_times[i] = current_time
                if remaining_burst_times[i] > time_quantum:
                    gantt_chart.append((i, current_time, current_time + time_quantum))
                    current_time += time_quantum
                    remaining_burst_times[i] -= time_quantum
                    process_queue.append(i)
                else:
                    gantt_chart.append((i, current_time, current_time + remaining_burst_times[i]))
                    current_time += remaining_burst_times[i]
                    remaining_burst_times[i] = 0
                    end_times[i] = current_time
                    completed += 1
            else:
                current_time += 1

        # Plot Gantt chart
        for (i, start, end) in gantt_chart:
            self.ax.barh(f"P{i+1}", end - start, left=start, color='pink')
        self.ax.set_title("Gantt Chart - Round Robin Scheduling")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Process")

        return start_times, end_times

    def srtf_scheduling(self, num_processes, arrival_times, burst_times):
        # Shortest Remaining Time First scheduling logic
        remaining_burst_times = burst_times[:]
        current_time = 0
        completed = 0
        n = len(arrival_times)
        gantt_chart = []
        start_times = [-1] * num_processes
        end_times = [0] * num_processes

        while completed < n:
            # Find the process with the shortest remaining burst time
            min_burst_time = float('inf')
            min_index = -1
            for i in range(num_processes):
                if arrival_times[i] <= current_time and remaining_burst_times[i] > 0 and remaining_burst_times[i] < min_burst_time:
                    min_burst_time = remaining_burst_times[i]
                    min_index = i

            if min_index == -1:
                current_time += 1
            else:
                if start_times[min_index] == -1:
                    start_times[min_index] = current_time
                gantt_chart.append((min_index, current_time, current_time + 1))
                remaining_burst_times[min_index] -= 1
                current_time += 1
                if remaining_burst_times[min_index] == 0:
                    end_times[min_index] = current_time
                    completed += 1

        # Plot Gantt chart
        for (i, start, end) in gantt_chart:
            self.ax.barh(f"P{i+1}", end - start, left=start, color='purple')
        self.ax.set_title("Gantt Chart - SRTF Scheduling")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Process")

        return start_times, end_times

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerApp(root)
    root.mainloop()
