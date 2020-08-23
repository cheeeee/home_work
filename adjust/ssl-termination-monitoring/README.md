#### Assumptions
##### Provided information:
A server with the following specs:

- 4 Intel(R) Xeon(R) CPU E7-4830 v4 @ 2.00GHz
- 64GB of ram
- 2 tb HDD disk space
- 2 x 10Gbit/s nics
##### Additional assumptions
- Partition schema: ESP partition on one of the disks, RAID1 with rootfs, UEFI boot.
- Up-to-date CentOS 8 with epel repo enabled
- Stock Linux kernel from CentOS
- No custom software
- 1st NIC used for incoming/outgoing connecting to the Internet, 2nd NIC used
for connection to the internal network with backends and services.

####  Answer
Monitoring for such server consist of 2 aspects:
* Data collection
* Visualizing/Alerts, disaster recovery and post-mortem

In my opinion, it would be enough to use Zabbix for such task.
We would not consider using any specific DB for Zabbix, so let`s stop on PostgreSQL.
Zabbix agent (PSK or CA need to be used for connecting to Server) need to be installed and configured on server and 
somewhere in the private network, there must be Zabbix Server.

### Data collection
Let`s split all metrics into few sections:
* I/O metrics
* Application-specific metrics
* OS/CPU/MEM metrics

##### IO
We need to collect such data:
* Number of packets processed by each NIC (incoming, outgoing)
* Traffic stats (bytes per second) for each NIC (RX, TX)
* I/O time for each disk (MB read, MB write, atime, etc)

##### OS, CPU, MEM
* Number of processes, their state (Z, D, R, S, T), virtual memory usage, actual memory usage, etc
* Number of TCP and UDP packets, errors on L4, other stats (like TCP syn), dropped packages
* L3 (IP) level errors
* L2 errors
* Average load
* Temperatures for different parts: PCI temp, NIC, CPU, MEM, etc
* Memory state (free, used, swapped, shared, buffered, available)
* CPU usage, including kernel CPU usage
* IRQ stats for devices\K modules (/proc/interrupts)
* Available entropy (since SSL entropy-heavy, in other systems it can be skipped)
* Context switch stats, NUMA stats (since we are on multi NUMA system)
* Free disk space and other FS metrics (free/used inodes, fragmentation, quotas, etc)
* mdadm stats, logical raid health
* Available updates, packages versions, rpm db state
* System daemons state, like SSHd

#### Application monitoring
* Active backends (system ping/heartbeat to backends, app metrics about backend) and number of backends
* TPS (Transaction per second)
* Latency for requests
* Rejected connections
* 5xx errors
* Number of connections
* Number of HTTP requests, other HTTP metrics (HTTP methods, status codes)
* RTT (Round trip time)

### Visualizing, alerts, post mortem
Few dashboards need to be created, one for NOCs (network IO), one for SREs (OS, APM) with respecting graphs.

Triggers need to be set for most critical parts of the system: CPU usage, high error rate, backend disconnecting, etc.
Different types of alerts need to be set, depending on the influence on system performance. The low number of NUMA 
memory miss does not require immediate actions and gathering meeting with Seniors SRE, uncles it dramatically increases errors rate or performance. When severe alerts occur more engineers need to involved to analyze the situation and deciding about next steps.

Disaster recovery plan needs to exist or need to be created after an incident during post-mortem.
Such a plan helps engineers to make a decision based on previous experience. 

### Possible challenges
First of all, application monitoring might not be that easy comparing to gathering OS metrics.
Imaging using Nginx for SSL offload. Nginx does not provide various SSL metrics by default, so it dev team might
need to write a custom Lua-based plugin to gather such metrics, for example for RTT.

Also, various metrics need to be calculated on Zabbix Server or agent, such as TPS and this involves creating custom 
graphs and items.

Also, it might be useful to create a network map with intermediate network devices (if they exist) and collect metrics from those devices as well (via SNMP for example). Severe incidents happening on application-level might be caused by
malfunctions/overload in intermediate devices, therefore using one utility for all monitoring will help the team to react faster and make the right decisions based on the big amount of collected data.

Also, the team need to monitor CVEs that affecting currently installed packages and act in case if there are any.

Anomaly detection can be used as well, it might involve Zabbix internal mechanics like hysteresis, prediction trigger 
or external tool can be used (it is possible to extract raw data from Zabbix DB).

