import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

parser=argparse.ArgumentParser(description ="TCP port Scanner")

parser.add_argument("target",help="Target IP address or hostname")
parser.add_argument("--start", type=int,default=1, help=" Starting port")
parser.add_argument("--end",type =int, default=1024, help="ending port")

args=parser.parse_args()

target=args.target

print("[*] Target:", target)

print(f"[*] port range: {args.start}-{args.end} ")
if(1 <= args.start <= 65535 and
    1 <= args.end <= 65535 and
    args.start <= args.end):
    pass
else:
    print("Invalid port range")
    if(args.start<1 or args.start>65535):
        print("Starting port should be between 1 and 65535")
    if(args.end<1 or args.end>65535):
        print("Ending port should be between 1 and 65535")      
    if(args.start > args.end):
        print("Starting port cannot be greater than ending port")
    exit(1)
def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"[+] Port {port} Open")
    except socket.timeout:
        pass
    except socket.error:
        pass
    finally:
        s.close()
print("[*] Scanning starts...")
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range(args.start, args.end+1))
print("[*] Scan complete ")
