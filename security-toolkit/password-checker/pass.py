password=input("Enter password: ")
has_up=False
has_low=False
has_dig=False
has_spec=False

score=0
for ch in password:
    if ch.isupper():
        has_up=True
    if ch.islower():
        has_low=True
    if ch.isdigit():
        has_dig=True
    if ch in "!@#$%^&*()_+-=[]{}|;':\",./<>?":
        has_spec=True
print("Password length:", len(password))
if len(password) >= 8:
    score+=1
    print("Password length is sufficient")
else:
    print("Password length is insufficient")
if has_up:
    score+=1
    print("Password has uppercase letter")
if has_low:
    score+=1
    print("Password has lowercase letter")
if has_dig:
    score+=1
    print("Password has digit")
if has_spec:
    score+=1
    print("Password has special character")
print("Password score:", score)
if score==5:
    print("Password is strong")
elif score==4:
    print("Password is good")
elif score==3:
    print("Password is moderate")
else:
    print("Password is weak")
common_passwords = [
    "password",
    "123456",
    "password123",
    "admin",
    "qwerty"
]
if password in common_passwords:
    print("Warning: This password is commonly used and may be easily guessed. Consider choosing a more unique password.")