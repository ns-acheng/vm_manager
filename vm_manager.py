import subprocess
import sys
import os
import logging
import threading
import getpass
from util_log import LogSetup
from util_input import WindowsInputMonitor

VMRUN_PATH = r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"

VM_PATHS = {
    "w1125h2": r"C:\vm\w1125h2\w1125h2.vmx",
}

def setup(vm_name):
    if not os.path.exists(VMRUN_PATH):
        logging.error(f"vmrun.exe not found at: {VMRUN_PATH}")
        return None

    vmx_path = VM_PATHS.get(vm_name)
    if not vmx_path:
        logging.error(f"VM '{vm_name}' not defined. Available: {list(VM_PATHS.keys())}")
        return None
        
    if not os.path.exists(vmx_path):
        logging.error(f"VMX file not found at: {vmx_path}")
        return None

    return vmx_path

def manage_vm_state(vm_name):
    vmx_path = setup(vm_name)
    if not vmx_path:
        return

    print(f"Preparing to monitor {vm_name}. Please enter the encrypted VM password if required.")
    try:
        vm_password = getpass.getpass("VM Password (press Enter if none): ")
    except Exception as e:
        logging.error(f"Failed to get password: {e}")
        vm_password = ""

    logging.info(f"Monitoring VM '{vm_name}'...")
    
    stop_event = threading.Event()
    input_monitor = WindowsInputMonitor()
    input_monitor.start_input_monitor(stop_event)
    
    restart_count = 0

    while not stop_event.is_set():
        try:
            check_cmd = [VMRUN_PATH, "list"]
            result = subprocess.run(check_cmd, capture_output=True, text=True)
            
            if vmx_path not in result.stdout:
                logging.info(f"VM '{vm_name}' not running. Waiting 10 seconds...")
                if stop_event.wait(10):
                    break
                
                if not stop_event.is_set():
                    restart_count += 1
                    logging.info(f"Starting {vm_name} (Restart count: {restart_count})...")
                    if vm_password:
                        start_cmd = [VMRUN_PATH, "-vp", vm_password, "start", vmx_path]
                    else:
                        start_cmd = [VMRUN_PATH, "start", vmx_path]
                    subprocess.run(start_cmd)
                
                logging.info("Waiting 10 seconds after start...")
                if stop_event.wait(10):
                    break
            else:
                if stop_event.wait(5):
                    break
                
        except Exception as e:
            logging.error(f"Error: {e}")
            if stop_event.wait(10):
                break
    
    logging.info(f"Exiting VM Manager loop. Total restarts: {restart_count}")

if __name__ == "__main__":
    log_setup = LogSetup()
    log_setup.setup_logging()

    if len(sys.argv) < 2:
        logging.error("Usage: python vm_manager.py <vmname>")
        sys.exit(1)
        
    manage_vm_state(sys.argv[1])