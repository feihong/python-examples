"""
Make sure that requests is installed with SOCKS support:

pip install requests[socks]

Make sure you've opened a connection to the proxy:

ssh -N -C -D <port> <ip_address>

"""
import requests

url = 'http://ipecho.net/plain'

print('Actual IP address:', requests.get(url).text)

proxies = {'http': 'socks5://localhost:15600'}
print('Proxy IP address:', requests.get(url, proxies=proxies).text)
