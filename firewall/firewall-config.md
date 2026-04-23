# 🔧 Firewall Configuration — Implementation Commands
 
 
## Firewall on RouterVM using Iptables Centralized)
 
 
**Note:** iptables rules are cleared on reboot. Use `iptables-persistent` to save them.
 
```bash
# Enable IP forwarding
sudo nano /etc/sysctl.conf
#Add
net.ipv4.ip_forward=1
#After editing, apply changes
sudo sysctl -p
 
# Set default DROP policy
sudo iptables -P FORWARD DROP
 
# Allow Web → API (port 5000)
sudo iptables -A FORWARD -s 192.168.30.0/24 -d 192.168.35.20 -p tcp --dport 5000 -j ACCEPT
sudo iptables -A FORWARD -s 192.168.35.20 -d 192.168.30.0/24 -p tcp --sport 5000 -j ACCEPT
 
# Allow API → Database (port 5432)
sudo iptables -A FORWARD -s 192.168.35.20 -d 192.168.40.20 -p tcp --dport 5432 -j ACCEPT
sudo iptables -A FORWARD -s 192.168.40.20 -d 192.168.35.20 -p tcp --sport 5432 -j ACCEPT
 
# Allow Management VM SSH to all machines (but no other SSH)
sudo iptables -A FORWARD -s 192.168.50.10 -p tcp --dport 22 -j ACCEPT
sudo iptables -A FORWARD -s 192.168.30.10 -s 192.168.35.20 -s 192.168.40.20 -p tcp --dport 22 -j DROP
sudo iptables -A FORWARD -p tcp --sport 22 -d 192.168.50.10 -j ACCEPT
 
# Block all other traffic
sudo iptables -A FORWARD -j DROP
 
# Save rules
sudo netfilter-persistent save
 
# Verify
sudo iptables -L -n -v
```
 
---
 
## Testing Rules
 
### From Web Server
 
```bash
# Should work: can reach API
curl http://192.168.35.20:5000/api/trades
 
# Should fail: cannot reach database directly (blocked)
nc -zv 192.168.40.20 5432  # Will timeout
 
# Should work: HTTP is allowed
curl http://localhost/
```
 
### From API Server
 
```bash
# Should work: can reach database
psql -h 192.168.40.20 -U trader -d trading_sheet -c "SELECT 1"
 
# Should work: can receive from web server
# (test by clicking Load Trades on web dashboard)
 
# Should fail: cannot reach web server directly
nc -zv 192.168.30.10 80  # Will timeout
```
 
### From Database Server
 
```bash
# Should work: can receive from API on port 5432
sudo netstat -tuln | grep 5432
 
# Should work: can receive SSH from management
# (ssh from 192.168.50.10)
 
# Should fail: cannot reach web server or API directly
nc -zv 192.168.30.10 80  # Will timeout
nc -zv 192.168.35.20 5000  # Will timeout
```
 
---
 
## Viewing/Modifying Rules
 
```bash
# View all rules
sudo iptables -L -n -v
 
# View INPUT chain only
sudo iptables -L INPUT -n -v
 
# View with line numbers (for deletion)
sudo iptables -L -n -v --line-numbers
 
# Delete a rule (by line number)
sudo iptables -D INPUT 3
 
# Flush all rules (WARNING: opens all ports!)
sudo iptables -F
 
# Save current rules
sudo netfilter-persistent save
```
 
---
 
## Troubleshooting
 
### Testing if a Port is Blocked
 
```bash
# From source VM, try to connect
nc -zv <destination_ip> <port>
 
# Or from destination VM, listen
nc -l <port>
# Then from source, try to connect
nc -zv <destination_ip> <port>
```
 
### Verify What's Allowed
 
```bash
# UFW
sudo ufw show added
 
# iptables
sudo iptables -L -n -v
sudo iptables -L -n -v --line-numbers
```
 
---
 
## Best Practices
 
1. **Start restrictive, then allow** — deny all, then whitelist what's needed
2. **Test after each rule** — don't apply 10 rules at once
3. **Document why each rule exists** — add comments
4. **Use specific IPs** — not 0.0.0.0/0 unless necessary
5. **SSH first** — always allow SSH from management before other rules
6. **Monitor rejected traffic** — `sudo tail -f /var/log/syslog | grep REJECT`
7. **Automate with Ansible** — don't manually configure each VM
---
 
## Common Mistakes
 
| Mistake | Impact | Fix |
|---------|--------|-----|
| Block SSH before allowing it | Locked out | Use VM console to fix |
| Default deny without allow rules | Nothing works | Add ACCEPT rules first |
| Block loopback (lo) | Services can't communicate internally | Always allow `lo` interface |
| Forget return traffic | Outbound works, inbound fails | Allow ESTABLISHED,RELATED |
| Rules not persistent | Settings lost on reboot | Use netfilter-persistent or ufw enable |
 
---
 
## Security Notes
 
- These rules assume internal network traffic is trusted
- For untrusted networks, encrypt traffic with TLS
- Consider DDoS protection on internet-facing (port 80) machine
- Monitor logs for suspicious connection attempts
- Regularly audit firewall rules for unnecessary entries
