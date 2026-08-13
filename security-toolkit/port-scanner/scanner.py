import socket
from concurrent.futures import ThreadPoolExecutor

target = input("Enter the target IP address: ")

def scan_port(port):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        result=s.connect_ex((target,port))
        if result==0:
            print(f"Port {port} is open")
    except:
        pass
    finally:
        s.close()

    #Threading part
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port,range(1,1025))
