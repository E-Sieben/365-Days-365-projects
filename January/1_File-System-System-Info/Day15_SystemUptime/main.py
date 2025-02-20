import psutil
from datetime import datetime

def show_uptime():
   uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
   print(f"System Uptime: {uptime}")
   return uptime

show_uptime()