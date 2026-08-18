import socket
import dns.resolver
def lookup_record(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []

domain=input("Enter domain: ")
try:
    ip = socket.gethostbyname(domain)
    print("Domain:", domain)
    print("IP:", ip)
    A =lookup_record(domain, "A")
    print("A records:")
    for record in A:
            print(record)
    AAAA =lookup_record(domain, "AAAA")
    print("AAAA records:")
    for record in AAAA:
            print(record)
    CNAME = lookup_record(domain, "CNAME")

    print("\nCNAME records:")
    if CNAME:
        for record in CNAME:
            print(record)
    else:
        print("No CNAME records found.")

   
    MX=lookup_record(domain, "MX")
    print("\nMX records:")
    for record in MX:
        print(record)
    TXT=lookup_record(domain, "TXT")
    print("\nTXT records:")
    for record in TXT:
        print(record)
    NS=lookup_record(domain, "NS")
    print("\nNS records:")
    for record in NS:
        print(record)


   
except socket.gaierror:
    print("Error: Could not resolve domain.")