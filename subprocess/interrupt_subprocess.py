"""
How to interrupt a child process started via subprocess.Popen().

"""
import subprocess
import time
import signal


cmd = ['python', 'infinite_hello.py', '731']
proc = subprocess.Popen(cmd)
time.sleep(4)
# proc.terminate()                   # will kill process unceremoniously
proc.send_signal(signal.SIGINT)     # acts as if Ctrl+C was sent
proc.wait()
