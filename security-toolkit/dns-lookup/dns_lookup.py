
import dns.resolver
def lookup_record(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []

domain=input("Enter domain: ")
print("Domain:", domain)
A =lookup_record(domain, "A")

if A:
    print("IP:",A[0])
    print("A records:")
    for record in A:
        print(record)
else:
    print("No A records found.")
AAAA =lookup_record(domain, "AAAA")
print("AAAA records:")
if AAAA:
    for record in AAAA:
        print(record)
else:
    print("No AAAA records found.")
CNAME = lookup_record(domain, "CNAME")

print("\nCNAME records:")
if CNAME:
    for record in CNAME:
        print(record)
else:
    print("No CNAME records found.")

   
MX=lookup_record(domain, "MX")
print("\nMX records:")
if MX:
    for record in MX:
        print(record)
else:
    print("No MX records found.")
TXT=lookup_record(domain, "TXT")
print("\nTXT records:")
if TXT:
    for record in TXT:
        print(record)
else:
    print("No TXT records found.")
NS=lookup_record(domain, "NS")
print("\nNS records:")
if NS:
    for record in NS:
        print(record)
else:
    print("No NS records found.")


   
