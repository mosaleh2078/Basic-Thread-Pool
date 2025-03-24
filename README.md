# Basic-Thread-Pool

This repo has two Python scripts (main.py and server.py) that show how to use thread pools to handle multiple tasks at once.

### main.py
This script creates a ThreadPool to manage multiple worker threads running CPU-heavy tasks. The *cpu_waster* function just makes threads sleep to simulate work being done.
### server.py
This is a **multi-threaded** server that listens for incoming connections, fetches exchange rates from an API, and sends back the results. It uses a thread pool to handle multiple clients efficiently.
## Features
- Custom Thread Pool: Manages worker threads efficiently.
- Task Scheduling: Uses *queue.Queue* to handle tasks.
- CPU-bound Task Execution: *main.py* simulates long-running processes.
- Multi-threaded Currency Exchange Server: *server.py* responds to clients with exchange rates.
- Handles Multiple Requests: Uses threading for smooth performance.

## Liecence
This project is open-source and available under the MIT License. Feel free to contribute!
