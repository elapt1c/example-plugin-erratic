"""
ERRATIC System Info Plugin — shows hostname and public IP address.
"""
import socket
from plugin_sdk import Plugin, Field

ui = [
    Field.section("Control"),
    Field.button("refresh", label="🔄 Get System Info"),
    Field.section("Output"),
    Field.output("info", label="System Info", height="150px"),
    Field.output("status", label="Status", height="30px"),
]

plugin = Plugin("sysinfo", "1.0", "Shows hostname and public IP address", ui, author="elapt1c")

@plugin.on_command("refresh")
def handle_refresh(args):
    import requests
    plugin.set_output("status", "Gathering system info...")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        try:
            public_ip = requests.get("https://api.ipify.org", timeout=5).text.strip()
        except:
            public_ip = "unreachable"
        info = f"Hostname: {hostname}\nLocal IP: {local_ip}\nPublic IP: {public_ip}"
        print(info)
        plugin.set_output("info", info)
        plugin.set_output("status", "Done")
    except Exception as e:
        plugin.set_output("status", f"Error: {e}")

plugin.run()
