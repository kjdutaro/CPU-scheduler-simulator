# CPU Scheduling Simulator

## Overview
The **CPU Scheduling Simulator** is a Python-based graphical application that demonstrates various CPU scheduling algorithms, both preemptive and non-preemptive. The simulator includes a friendly user interface, built using Tkinter, which allows users to input scheduling parameters and visualize the Gantt chart and other metrics, such as Turnaround Time (TAT) and Waiting Time (WT), for each scheduling algorithm.

## Features
- **Non-Preemptive Scheduling Algorithms**:
  1. **First-Come-First-Serve (FCFS)**
  2. **Shortest Job First (SJF)**
  3. **Priority Scheduling**

- **Preemptive Scheduling Algorithms**:
  1. **Round Robin (RR)**
  2. **Shortest Remaining Time First (SRTF)**

- **User Interface**: Allows the user to easily input scheduling parameters, select the scheduling algorithm, and visualize the Gantt chart along with other metrics.

## Requirements
- **Python 3.x**
- **Tkinter** (comes pre-installed with Python)
- **Matplotlib** (for Gantt chart visualization)

To install Matplotlib, run the following command:
```sh
pip install matplotlib
```

## GitHub Repository
You can find the source code on GitHub: [GitHub Repository Link](https://github.com/kjdutaro/CPU-scheduler-simulator)

## Usage Instructions
1. **Download** the ZIP file of the project.
2. **Extract the ZIP file** to your desired location and **navigate to the extracted folder**.
3. **Run the Application**:
   ```sh
   python script.py
   ```
4. **User Inputs**:
   - **Select Scheduling Algorithm**: Choose the desired CPU scheduling algorithm from the dropdown.
   - **Enter Parameters**:
     - **Number of Processes**: Total number of processes to be scheduled.
     - **Arrival Times**: Comma-separated list of arrival times for each process.
     - **Burst Times**: Comma-separated list of burst times for each process.
     - **Priorities**: Comma-separated list of priorities (required for Priority Scheduling).
     - **Time Quantum**: Time quantum for Round Robin scheduling.
5. **Simulate Scheduling**: Click on the "Simulate Scheduling" button to generate the Gantt chart and display metrics such as TAT and WT.

## Sample Inputs

Sample Inputs:
- **Number of Processes**: `8`
- **Arrival Times**: `0, 2, 4, 6, 8, 10, 12, 14`
- **Burst Times**: `5, 3, 8, 6, 7, 4, 5, 2`
- **Priorities** (only needed for Priority Scheduling): `3, 1, 4, 2, 5, 2, 3, 1` (lower value means higher priority)
- **Time Quantum** (only needed for Round Robin): `3`

Another Sample Inputs:
- **Number of Processes**: `12`
- **Arrival Times**: `0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21`
- **Burst Times**: `6, 4, 8, 3, 7, 5, 6, 4, 3, 9, 2, 5`
- **Priorities** (only needed for Priority Scheduling): `1, 3, 2, 5, 4, 1, 2, 3, 4, 5, 2, 1` (lower value means higher priority)
- **Time Quantum** (only needed for Round Robin): `5`

## Output
- **Gantt Chart**: Displays the execution order and duration of processes on a timeline.
- **Metrics Table**: Shows Turnaround Time (TAT) and Waiting Time (WT) for each process, along with the average TAT and WT.
