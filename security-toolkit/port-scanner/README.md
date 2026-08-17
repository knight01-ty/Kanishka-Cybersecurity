# How I Built a Python TCP Port Scanner

A basic TCP port scanner built with Python to understand
TCP/IP networking, socket programming, concurrency, and
network reconnaissance.

## Project Overview

This project started as a simple Python script that checked
TCP ports and gradually evolved into a command-line tool with:

- Command-line arguments
- Custom port ranges
- Timeout handling
- Error handling
- Input validation
- Concurrent scanning
- Clean CLI output

## Technologies

- Python 3
- Socket Programming
- TCP/IP
- argparse
- ThreadPoolExecutor

**How I Built a Python TCP Port Scanner

Author: Kanishka Tyagi
Project: Python TCP Port Scanner
Language: Python
Focus: Networking & Cybersecurity

1. Problem

In cybersecurity, understanding what network services are exposed on a system is an important part of network reconnaissance.

A computer can have multiple network services running simultaneously. These services listen for incoming connections on different ports.

For example:

IP Address: 192.168.1.20


Port 22  → SSH
Port 80  → HTTP
Port 443 → HTTPS

The problem I wanted to solve was simple:

Can I build a Python program that checks a range of TCP ports and identifies which ones are accepting connections?

Instead of using an existing security tool, I decided to build a basic TCP port scanner myself to understand the networking concepts behind port scanning.

2. TCP/IP Basics

Before building the scanner, I needed to understand how computers communicate over networks.

IP Address

An IP address identifies a host on a network.

For example:

127.0.0.1

is the loopback address, meaning the computer itself.

When testing my scanner, I primarily used 127.0.0.1 so that I was scanning my own machine.

Ports

A port identifies a particular communication endpoint on a host.

The combination:

127.0.0.1:80

can be thought of as:

127.0.0.1 → Which computer?
80         → Which port?

Ports range from:

0–65535

My scanner allows scanning ports from 1 to 65535, with the default range being 1–1024.

3. TCP

My scanner uses TCP (Transmission Control Protocol).

TCP is connection-oriented, meaning a client attempts to establish a connection with a server before exchanging data.

For my scanner, the basic idea is:

Scanner
   │
   │ TCP connection attempt
   ▼
Target IP : Port
   │
   ├── Connection accepted → Port is open
   │
   └── Connection refused/unsuccessful → Port isn't accepting connections

I used TCP because attempting to establish a TCP connection provides a straightforward way to determine whether a TCP service is accepting connections on a particular port.

4. Python Sockets

Python provides the socket module for network communication.

I created a TCP socket using:

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

There are two important parameters here.

AF_INET

This specifies that I'm using IPv4 addressing.

SOCK_STREAM

This specifies a stream socket, which is used for TCP communication.

Therefore:

socket.AF_INET

means IPv4, while:

socket.SOCK_STREAM

means TCP-style stream communication.

5. Scanning Methodology

The scanner follows a relatively simple methodology.

For every port in the selected range:

Create a TCP socket.
Set a timeout.
Attempt to connect to the target and port.
Check the result.
Report an open port.
Close the socket.

Conceptually:

Target + Port
      ↓
Create TCP socket
      ↓
Set timeout
      ↓
Attempt connection
      ↓
Connection successful?
      │
   ┌──┴──┐
  YES    NO
   ↓      ↓
 OPEN   Continue
   ↓
Close socket
6. Implementing the Scanner

The first version of my scanner was very simple.

The user entered the target IP address, and the program scanned ports from 1 to 1024.

The core scanning operation used:

result = s.connect_ex((target, port))

connect_ex() attempts to establish a connection and returns a result code rather than directly raising an exception for every unsuccessful connection.

I used:

if result == 0:
    print(f"Port {port} is open")

A return value of 0 indicates that the connection attempt succeeded.

7. Timeout Handling

A network connection can sometimes take longer than expected.

Without a timeout, the scanner could spend too much time waiting for an individual connection attempt.

I therefore used:

s.settimeout(0.5)

This gives the connection attempt a maximum waiting period of approximately 0.5 seconds.

I also added specific exception handling:

except socket.timeout:
    pass


except socket.error:
    pass

This is better than using a completely generic:

except:
    pass

because the program now explicitly handles socket-related problems.

8. Adding Command-Line Arguments

The original version used:

input()

to obtain the target.

I later improved the scanner using Python's argparse module.

The scanner can now be executed like:

python scanner.py 127.0.0.1 --start 20 --end 80

Here:

127.0.0.1 → target
20        → starting port
80        → ending port

This made the scanner more flexible and more appropriate for a command-line security tool.

I also provided default values:

Start → 1
End   → 1024

So the user can simply run:

python scanner.py 127.0.0.1

and scan the default range.

9. Port Range Validation

I didn't want the scanner to accept obviously invalid ranges.

For example:

--start 500 --end 100

doesn't make sense because the starting port is greater than the ending port.

I therefore added validation requiring:

1 ≤ start ≤ 65535
1 ≤ end ≤ 65535
start ≤ end

If the input is invalid, the program displays an appropriate error message and terminates instead of attempting the scan.

This was one of the improvements that helped turn the project from a basic script into a more structured command-line tool.

10. Concurrent Scanning

Scanning ports sequentially can take longer because network operations involve waiting.

My original implementation used:

ThreadPoolExecutor(max_workers=100)

I then distributed the port-scanning tasks across the worker threads:

executor.map(
    scan_port,
    range(args.start, args.end + 1)
)

Instead of waiting for one port to completely finish before attempting another, multiple connection attempts can be in progress concurrently.

Conceptually:

Sequential:


Port 1 → Port 2 → Port 3 → Port 4
                 ↓
              Slower




Concurrent:


Port 1 ──────┐
Port 2 ──────┤
Port 3 ──────┤ → Multiple operations in progress
Port 4 ──────┘

This significantly improves the practical speed of a network scanner.

11. Resource Management

After each connection attempt, I close the socket:

finally:
    s.close()

The finally block is useful because it runs regardless of whether the connection attempt succeeds or encounters an exception.

This ensures that sockets don't remain open unnecessarily.

12. Testing

I tested the scanner against my own machine using:

127.0.0.1

This allowed me to experiment safely without scanning systems that I didn't own or have permission to test.

Testing a specific range

For example:

python scanner.py 127.0.0.1 --start 20 --end 80

The scanner reported the target and selected range and completed the scan.

Testing invalid input

I also tested:

python scanner.py 127.0.0.1 --start 500 --end 100

The program correctly reported:

Invalid port range
Starting port cannot be greater than ending port

and terminated without starting the scan.

This confirmed that the input-validation logic was working.

13. What I Learned

Building this project helped me connect theoretical networking concepts with actual Python code.

The main concepts I learned were:

IPv4 addressing
TCP
Ports
Client-server communication
Sockets
TCP connection attempts
Timeouts
Exception handling
Concurrent execution
Command-line arguments
Input validation
Resource management
Git/GitHub workflow

One of the most important lessons was that writing the code is only part of building a project.

I also needed to understand why each component existed.

For example:

socket.AF_INET

isn't just something I copied into the program—it tells the socket to use IPv4.

Similarly:

socket.SOCK_STREAM

specifies a stream socket appropriate for TCP.

14. Limitations

This is a basic educational TCP port scanner, not a replacement for professional network-scanning tools.

Some limitations include:

1. TCP only

The scanner currently focuses on TCP connections.

It does not perform UDP scanning.

2. Basic port detection

It determines whether a TCP connection can be established, but it doesn't perform detailed service identification.

3. No service/version detection

For example, it doesn't identify whether an open port is running:

Apache
Nginx
OpenSSH

or another service.

4. No banner grabbing

The scanner doesn't retrieve application banners or service information.

5. Limited output

It currently reports open ports but doesn't generate detailed scan reports.

6. Basic error handling

Socket errors are handled quietly rather than being reported in detail.

These limitations are intentional because my goal at this stage was to understand the fundamentals rather than immediately build a huge tool.

15. Future Improvements

Possible future improvements include:

Short-term
Better output formatting
More detailed error reporting
Scan statistics
Improved documentation
Cleaner project structure
Later
Service detection
Banner grabbing
UDP scanning
Configurable timeout
Exporting results to a file
More advanced concurrency control

However, I want to add these features gradually and understand each one before implementing it.

16. Final Architecture

The current scanner can be summarized as:

                 User
                  │
                  ▼
          Command-line arguments
                  │
                  ▼
             Input validation
                  │
                  ▼
              Target + Range
                  │
                  ▼
          ThreadPoolExecutor
                  │
          ┌───────┼───────┐
          ▼       ▼       ▼
        Port     Port    Port
          │       │       │
          ▼       ▼       ▼
       TCP socket connections
                  │
                  ▼
           Open / unsuccessful
                  │
                  ▼
              Clean output
17. Conclusion

Building this TCP port scanner was my first practical project focused on understanding network security through Python.

The project started as a simple script that checked ports sequentially. I then progressively improved it by adding:

Command-line arguments
        ↓
Custom port ranges
        ↓
Timeout handling
        ↓
Error handling
        ↓
Input validation
        ↓
Concurrent scanning
        ↓
Cleaner CLI output

The most valuable part of the project wasn't simply having a working port scanner. It was understanding the networking concepts behind it and learning how Python can interact with those concepts.

This project gives me a foundation for moving toward more advanced cybersecurity topics such as network reconnaissance, service enumeration, home SOC labs, and CTF-based learning.

The goal wasn't to build the most powerful scanner. The goal was to understand how one works.

## Usage

Run the scanner with:

```bash
python scanner.py 127.0.0.1

📌 Portfolio project summary

Project: Python TCP Port Scanner
Technologies: Python, Socket Programming, TCP/IP, argparse, ThreadPoolExecutor
Key concepts: Networking, TCP, IPv4, ports, sockets, concurrency, exception handling, input validation
Status: Working educational security tool

GitHub: Kanishka-Cybersecurity/security-toolkit/port-scanner