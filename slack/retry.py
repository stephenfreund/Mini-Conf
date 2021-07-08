import time
import sys

def retry(n, message, f):
    while True:
        try:
            return f()
        except:
            if n == 0:
                raise sys.exc_info()[0]
            print(f"Retrying {message}")
            n = n - 1
            time.sleep(1)
