"""
Get an unused port and print it.

"""
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 0))
port = s.getsockname()[1]
s.close()
print('Unused port:', port)
