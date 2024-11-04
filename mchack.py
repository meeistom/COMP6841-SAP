# McHack
import os
import requests
import nmap

def get_ips():
    ip_mac_type_str = os.popen('arp -a').read()
    return [line.strip() for line in ip_mac_type_str.strip().split('\n')]

def get_device_vendor(mac):
    url = f'https://api.macvendors.com/{mac}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return (response.status_code, response.text)
        else:
            return (response.status_code, 'Unknown')
    except requests.RequestException as e:
        return f"Error: {e}"

def get_target_ip(ip_mac_type_lst):
    ip_mac_type_dct = {}

    i = 1
    for line in ip_mac_type_lst:
        pre = ''
        suf = ''
        if len(line) <= 0:
            pass
        elif line[0] in ('0', '1', '2'):
            pre = f'{i}.\t'

            while True:
                res = get_device_vendor(line.split()[1])
                if res[0] == 429:
                    continue
                break
            ip_mac_type_dct[i] = line
            i += 1
            suf = f'\t{res[1]}'
        elif line.split()[0] == 'Internet':
            pre = '\t'
            suf = '\tVendor'
        print(pre + line + suf)

    while True:
        try:
            target_ip = int(input(f'Choose an IP address to attack (1 - {i-1}): '))
        except ValueError:
            print(f'IP address must be an integer.')
            continue

        if 1 > target_ip or target_ip > i-1:
            print(f'IP address must be in the specified range.')
            continue

        break

    return ip_mac_type_dct[target_ip].split()[0]

def get_open_ports(ip):
    print(f'{ip}: Scanning ports...')
    scanner = nmap.PortScanner()
    scanner.scan(ip)

    try:
        for protocol in scanner[ip].all_protocols():
            ports = scanner[target_ip][protocol]
    except KeyError:
        print('Could not retrieve ports')
        exit(0)

    print('Ports')
    print(f'port\tstate\treason\tname')
    i = 1
    for key in ports.keys():
        print(f'{i}.\t{key}\t{ports[key]['state']}\t{ports[key]['reason']}\t{ports[key]['name']}')
        i += 1

    while True:
        try:
            target_port = int(input(f'Choose a port to attack: '))
        except ValueError:
            print(f'Port must be an integer.')
            continue

        if target_port not in ports.keys():
            print(f'Port must be one of the following values: {', '.join([str(k) for k in ports.keys()])}')
            continue

        break

    return target_port





if __name__ == '__main__':
    print('''Hi, welcome to Macca's. What can I get for you today?
        
Uhh, could I get a
███╗   ███╗ ██████╗██╗  ██╗ █████╗  ██████╗██╗  ██╗
████╗ ████║██╔════╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝
██╔████╔██║██║     ███████║███████║██║     █████╔╝ 
██║╚██╔╝██║██║     ██╔══██║██╔══██║██║     ██╔═██╗ 
██║ ╚═╝ ██║╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
please?

That'll be $19.99, when you're ready.

---------------------------------------------------
          
Scanning IP's...
''')
    ip_lst = get_ips()
    target_ip = get_target_ip(ip_lst)
    target_port = get_open_ports(target_ip)
    print(target_port)
