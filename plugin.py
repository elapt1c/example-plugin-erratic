"""
ERRATIC Plugin — System Info
Shows the target hostname and public IP address.
"""

import socket
import urllib.request
from plugin_sdk import Plugin, Field

plugin = Plugin(
    name="sysinfo",
    version="1.0",
    description="Shows hostname and public IP address",
    ui_schema=[
        {"type": "section", "label": "Control"},
        {"type": "button", "name": "refresh", "label": "🔄 Get System Info"},
        {"type": "section", "label": "Output"},
        {"type": "output", "name": "info", "label": "System Info", "height": "150px", "format": "text"},
        {"type": "output", "name": "status", "label": "Status", "height": "30px", "format": "text"},
    ],
    author="elapt1c",
)

@plugin.on_command("refresh")
def cmd_refresh(args):
    plugin.set_output("status", "Fetching info...")
    lines = []

    # Hostname
    try:
        hostname = socket.gethostname()
        lines.append(f"Hostname: {hostname}")
    except Exception as e:
        lines.append(f"Hostname: error ({e})")

    # Local IPs
    try:
        local_ips = socket.gethostbyname_ex(hostname)
        for ip in local_ips[2]:
            lines.append(f"Local IP: {ip}")
    except Exception:
        lines.append("Local IP: could not resolve")

    # Public IP
    try:
        pub_ip = urllib.request.urlopen("https://api.ipify.org", timeout=10).read().decode()
        lines.append(f"Public IP: {pub_ip}")
    except Exception as e:
        lines.append(f"Public IP: error ({e})")

    plugin.set_output("info", "\n".join(lines))
    plugin.set_output("status", "✓ Done")

if __name__ == "__main__":
    plugin.run()
