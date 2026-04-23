# 🔧 Firewall Configuration — Implementation Commands
 
## Quick Choice
 
- **Want simple?** Use **UFW** (Option 1)
- **Want persistent/powerful?** Use **iptables** (Option 2)
- **Multiple VMs?** Use **Router Firewall** (Option 3)
---
 
## OPTION 1: UFW (Simple & Recommended)
 
### Web Server (192.168.30.10)
 
```bash
# Enable UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw enable
 
# Allow inbound HTTP from anywhere
sudo ufw allow 80/tcp
 
# Allow inbound SSH from Management VM only
sudo ufw allow from 192.168.50.10 to any port 22 proto tcp
 
# Allow outbound to API server on port 5000
sudo ufw allow out to 192.168.35.20 port 5000 proto tcp
 
# Verify
sudo ufw status
```
 
### API Server (192.168.35.20)
 
```bash
# Enable UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw enable
 
# Allow inbound from Web server on port 5000
sudo ufw allow from 192.168.30.10 to any port 5000 proto tcp
 
# Allow inbound SSH from Management VM only
sudo ufw allow from 192.168.50.10 to any port 22 proto tcp
 
# Allow outbound to Database server on port 5432
sudo ufw allow out to 192.168.40.20 port 5432 proto tcp
 
# Verify
sudo ufw status
```
 
### Database Server (192.168.40.20)
 
```bash
# Enable UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw enable
 
# Allow inbound from API server on port 5432
sudo ufw allow from 192.168.35.20 to any port 5432 proto tcp
 
# Allow inbound SSH from Management VM only
sudo ufw allow from 192.168.50.10 to any port 22 proto tcp
 
# Verify
sudo ufw status
```
 
### Management VM (192.168.50.10)
 
```bash
# Enable UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw enable
 
# Block all inbound SSH (management VM only initiates connections)
# (nothing to add - default deny incoming blocks SSH)
 
# Allow outbound SSH to all machines
sudo ufw allow out to 192.168.30.10 port 22 proto tcp  # Web server
sudo ufw allow out to 192.168.35.20 port 22 proto tcp  # API server
sudo ufw allow out to 192.168.40.20 port 22 proto tcp  # Database server
 
# Verify
sudo ufw status
```
 
---
 
## OPTION 2: iptables (Powerful & Persistent)
 
**Note:** iptables rules are cleared on reboot. Use `iptables-persistent` to save them.
 
### Web Server (192.168.30.10)
 
```bash
# Install persistence
sudo apt install iptables-persistent -y
 
# Set default policies
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
 
# Allow loopback traffic
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
 
# Allow established connections
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
 
# Allow inbound HTTP
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
 
# Allow inbound SSH from Management VM only
sudo iptables -A INPUT -s 192.168.50.10 -p tcp --dport 22 -j ACCEPT
 
# Allow outbound to API server
sudo iptables -A OUTPUT -d 192.168.35.20 -p tcp --dport 5000 -j ACCEPT
 
# Save rules
sudo netfilter-persistent save
sudo systemctl enable netfilter-persistent
 
# Verify
sudo iptables -L -n
```
 
### API Server (192.168.35.20)
 
```bash
# Install persistence
sudo apt install iptables-persistent -y
 
# Set default policies
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
 
# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
 
# Allow established connections
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
 
# Allow inbound from Web server on port 5000
sudo iptables -A INPUT -s 192.168.30.10 -p tcp --dport 5000 -j ACCEPT
 
# Allow inbound SSH from Management VM only
sudo iptables -A INPUT -s 192.168.50.10 -p tcp --dport 22 -j ACCEPT
 
# Allow outbound to Database on port 5432
sudo iptables -A OUTPUT -d 192.168.40.20 -p tcp --dport 5432 -j ACCEPT
 
# Save rules
sudo netfilter-persistent save
sudo systemctl enable netfilter-persistent
 
# Verify
sudo iptables -L -n
```
 
### Database Server (192.168.40.20)
 
```bash
# Install persistence
sudo apt install iptables-persistent -y
 
# Set default policies
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
 
# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
 
# Allow established connections
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
 
# Allow inbound from API server on port 5432
sudo iptables -A INPUT -s 192.168.35.20 -p tcp --dport 5432 -j ACCEPT
 
# Allow SSH from Management VM only
sudo iptables -A INPUT -s 192.168.50.10 -p tcp --dport 22 -j ACCEPT
 
# Save rules
sudo netfilter-persistent save
sudo systemctl enable netfilter-persistent
 
# Verify
sudo iptables -L -n
```
 
### Management VM (192.168.50.10)
 
```bash
# Install persistence
sudo apt install iptables-persistent -y
 
# Set default policies
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
 
# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
 
# Allow established connections
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
 
# Allow outbound SSH to all machines (no inbound SSH allowed)
sudo iptables -A OUTPUT -d 192.168.30.10 -p tcp --dport 22 -j ACCEPT  # Web server
sudo iptables -A OUTPUT -d 192.168.35.20 -p tcp --dport 22 -j ACCEPT  # API server
sudo iptables -A OUTPUT -d 192.168.40.20 -p tcp --dport 22 -j ACCEPT  # Database server
 
# Save rules
sudo netfilter-persistent save
sudo systemctl enable netfilter-persistent
 
# Verify
sudo iptables -L -n
```
 
---
 
## OPTION 3: Router Firewall (Centralized)
 
If you have a dedicated Router VM connecting all networks:
 
```bash
# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
 
# Set default policies
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
 
### UFW
 
```bash
# View rules
sudo ufw status numbered
 
# Delete a rule
sudo ufw delete allow 80/tcp
 
# Reload
sudo ufw reload
 
# Disable temporarily (emergency access)
sudo ufw disable
 
# Re-enable
sudo ufw enable
```
 
### iptables
 
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
 
### Rules Not Persisting After Reboot
 
```bash
# UFW
sudo ufw enable  # Re-enable UFW
 
# iptables
sudo netfilter-persistent save
sudo systemctl enable netfilter-persistent
```
 
### Accidentally Locked Out (SSH not working)
 
On the VM console:
```bash
# UFW
sudo ufw disable
 
# iptables
sudo iptables -F  # Flush all rules
```
 
Then reconfigure properly.
 
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
