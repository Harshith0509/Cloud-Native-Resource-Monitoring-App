from flask import Flask, render_template
import psutil
import time
from datetime import datetime

app = Flask(__name__)

def get_system_metrics():
    # CPU metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else "N/A"

    # Memory metrics
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    mem_used = mem.used / (1024 ** 3) 
    mem_total = mem.total / (1024 ** 3) 

    # Disk metrics
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_used = disk.used / (1024 ** 3)  
    disk_total = disk.total / (1024 ** 3)  

    # Network metrics
    net = psutil.net_io_counters()
    bytes_sent = net.bytes_sent / (1024 ** 2)  
    bytes_recv = net.bytes_recv / (1024 ** 2)  

    # Alerts
    alerts = []
    if cpu_percent > 80:
        alerts.append("High CPU utilization detected!")
    if mem_percent > 80:
        alerts.append("High Memory utilization detected!")
    if disk_percent > 80:
        alerts.append("High Disk utilization detected!")

    return {
        'cpu_percent': cpu_percent,
        'cpu_count': cpu_count,
        'cpu_freq': cpu_freq,
        'mem_percent': mem_percent,
        'mem_used': round(mem_used, 2),
        'mem_total': round(mem_total, 2),
        'disk_percent': disk_percent,
        'disk_used': round(disk_used, 2),
        'disk_total': round(disk_total, 2),
        'bytes_sent': round(bytes_sent, 2),
        'bytes_recv': round(bytes_recv, 2),
        'alerts': alerts,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/')
def index():
    metrics = get_system_metrics()
    return render_template('index.html', **metrics)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)