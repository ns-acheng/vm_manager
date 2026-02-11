# VM Manager

This utility continuously monitors the state of a specified VMware Virtual Machine and automatically restarts it if it is not running (e.g., if it sleeps or crashes).

## Prerequisites

*   **Python 3.x**
*   **VMware Workstation** installed.
*   The `vmrun.exe` command-line utility (usually included with VMware Workstation).

## Configuration

1.  Open `vm_manager.py`.
2.  Update the `VMRUN_PATH` variable if your installation of VMware Workstation is in a custom location.
    ```python
    VMRUN_PATH = r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"
    ```
3.  Add your VMs to the `VM_PATHS` dictionary inside `vm_manager.py`. Use a friendly name (key) and the full path to the `.vmx` file (value).
    ```python
    VM_PATHS = {
        "w1125h2": r"C:\vm\w1125h2\w1125h2.vmx",
        "ubuntu": r"C:\vm\ubuntu\my_ubuntu.vmx",
    }
    ```

## Usage

Run the script from the command line, providing the name of the VM you want to monitor (as defined in `VM_PATHS`).

```powershell
python vm_manager.py <vmname>
```

**Example:**

```powershell
python vm_manager.py w1125h2
```

## Features

*   **Monitoring**: Checks runs `vmrun list` continuously to see if the target VM is running.
*   **Auto-Start**: If the VM stops, it waits 10 seconds, restarts it, and waits another 10 seconds before resuming monitoring.
*   **Logging**: Logs are saved to a timestamped file in the `log/` directory and printed to the console.
*   **Clean Exit**: Press `ESC` or `Ctrl+C` to gracefully stop the monitoring loop.
