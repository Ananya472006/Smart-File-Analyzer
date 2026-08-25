import sys
import platform
import psutil

def get_os_info():
    """Retrieves Operating System and Python environment information."""
    try:
        return {
            "Operating System": platform.system(),
            "OS Version": platform.version(),
            "OS Release": platform.release(),
            "Machine": platform.machine(),
            "Architecture": platform.architecture()[0],
            "Processor": platform.processor() or "N/A",
            "Python Version": sys.version.split(" ")[0]
        }
    except Exception as e:
        return {
            "Operating System": "N/A",
            "OS Version": "N/A",
            "OS Release": "N/A",
            "Machine": "N/A",
            "Architecture": "N/A",
            "Processor": "N/A",
            "Python Version": sys.version.split(" ")[0]
        }

def get_cpu_info():
    """Retrieves CPU core count, frequency, and usage statistics."""
    try:
        logical_cores = psutil.cpu_count(logical=True) or 1
        physical_cores = psutil.cpu_count(logical=False) or 1
        cpu_usage = psutil.cpu_percent(interval=0.1)
        
        freq_str = "N/A"
        try:
            freq = psutil.cpu_freq()
            if freq and freq.current:
                freq_str = f"{freq.current:.2f} MHz"
        except Exception:
            freq_str = "N/A"

        return {
            "Physical Cores": physical_cores,
            "Logical Cores": logical_cores,
            "CPU Usage (%)": cpu_usage,
            "CPU Frequency": freq_str
        }
    except Exception as e:
        return {
            "Physical Cores": 1,
            "Logical Cores": 1,
            "CPU Usage (%)": 0.0,
            "CPU Frequency": "N/A"
        }

def get_memory_info():
    """Retrieves system RAM total, used, available, and usage percentage."""
    try:
        mem = psutil.virtual_memory()
        def bytes_to_gb(b):
            return round(b / (1024 ** 3), 2)

        return {
            "Total RAM (GB)": bytes_to_gb(mem.total),
            "Used RAM (GB)": bytes_to_gb(mem.used),
            "Available RAM (GB)": bytes_to_gb(mem.available),
            "RAM Usage (%)": mem.percent
        }
    except Exception as e:
        return {
            "Total RAM (GB)": 0.0,
            "Used RAM (GB)": 0.0,
            "Available RAM (GB)": 0.0,
            "RAM Usage (%)": 0.0
        }

def get_disk_info():
    """Retrieves primary disk partition space metrics."""
    try:
        # Default to root or current working drive
        mountpoint = "C:\\" if platform.system() == "Windows" else "/"
        usage = psutil.disk_usage(mountpoint)

        def bytes_to_gb(b):
            return round(b / (1024 ** 3), 2)

        return {
            "Mountpoint": mountpoint,
            "Total Disk Space (GB)": bytes_to_gb(usage.total),
            "Used Disk Space (GB)": bytes_to_gb(usage.used),
            "Free Disk Space (GB)": bytes_to_gb(usage.free),
            "Disk Usage (%)": usage.percent
        }
    except Exception as e:
        return {
            "Mountpoint": "N/A",
            "Total Disk Space (GB)": 0.0,
            "Used Disk Space (GB)": 0.0,
            "Free Disk Space (GB)": 0.0,
            "Disk Usage (%)": 0.0
        }

def get_complete_system_info():
    """Compiles complete system information payload."""
    return {
        "os": get_os_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info()
    }
