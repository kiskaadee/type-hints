# Network Firewall logs
# TODO: Annotate these homogeneous collections (list of strings, set of strings).
active_ips: list[str] = ["192.168.1.1", "10.0.0.5"]
blocked_ips: set[str] = {"172.16.0.2", "192.168.1.100"}

# Logic block checking if a connection is secure
client_ip = "10.0.0.5"
if client_ip in active_ips and client_ip not in blocked_ips:
    print("Secure connection allowed.")
