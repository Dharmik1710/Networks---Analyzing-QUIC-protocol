#!/usr/bin/env python
import os

import argparse
from mininet.net import Containernet
from mininet.node import Controller, Docker
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import atexit
import os

# Global list to track created containers
created_containers = []


def track_container(container_name):
    """Track the name of a container for cleanup."""
    created_containers.append(container_name)


def cleanup():
    """Cleanup function to stop and remove only tracked containers."""
    info("*** Cleaning up script-created containers and network...\n")
    for container in created_containers:
        os.system(f"docker rm -f {container} 2>/dev/null || true")
    os.system("mn -c 2>/dev/null || true")


def setup_network(bw_client=20, latency_client="80ms", region="India"):
    net = Containernet(controller=Controller)

    info("*** Adding controller\n")
    net.addController("c0")

    info("*** Adding switches\n")
    s1 = net.addSwitch("s1")  # Client switch
    s2 = net.addSwitch("s2")  # Server switch
    s3 = net.addSwitch('s3')  # internal network switch

    info("*** Adding router\n")
    r1 = net.addHost("r1", ip="10.0.0.254")

    info("*** Adding clients\n")


    h1 = net.addDocker("h1", ip="10.0.0.1/24", dimage="host-web-image", volumes=[f"{os.getcwd()}/../stats/assets/pcaps:/pcaps:rw"]
    # , dcmd=f"/bin/bash curl_request.sh --region {region} --iterations 3"
    )
    track_container("h1")
    
    h2 = net.addDocker("h2", ip="10.0.0.2/24", dimage="host-image")
    track_container("h2")

    info("*** Adding servers\n")

    # Server 1
    srv1_proxy = net.addDocker(
        "srv1-proxy",
        ip="10.0.1.1/24",
        dimage="proxy-server-image",
        ports=[443],
        port_bindings={443: 8443},
        dcmd="caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"
    )
    track_container("srv1-proxy")

    srv1_web = net.addDocker("srv1-web", ip="192.168.1.2/24", dimage="web-server-image", dcmd="node /usr/src/app/app.js")
    track_container("srv1-web")

    srv1_video = net.addDocker("srv1-video", ip="192.168.1.3/24", dimage="video-server-image", dcmd="node /usr/src/app/app.js")
    track_container("srv1-video")

    # Server 2
    srv2_proxy = net.addDocker(
        "srv2-proxy",
        ip="10.0.1.2/24",
        dimage="proxy-server-image",
        ports=[443],
        port_bindings={443: 9443},
        dcmd="caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"
    )
    track_container("srv2-proxy")

    srv2_web = net.addDocker("srv2-web", ip="192.168.2.2/24", dimage="web-server-image", dcmd="node /usr/src/app/app.js")
    track_container("srv2-web")

    srv2_video = net.addDocker("srv2-video", ip="192.168.2.3/24", dimage="video-server-image", dcmd="node /usr/src/app/app.js")
    track_container("srv2-video")

    info("*** Creating links\n")

    # Client links
    net.addLink(h1, s1, cls=TCLink, bw=bw_client, delay=latency_client, use_htb=True, params1={'quantum': 1500})
    net.addLink(h2, s1, cls=TCLink, bw=bw_client, delay=latency_client, use_htb=True, params1={'quantum': 1500})
    net.addLink(s1, r1, cls=TCLink, bw=bw_client, delay=latency_client, use_htb=True, params1={'quantum': 1500})

    # Connect srv1-proxy, srv1-web, and srv1-video to s3
    net.addLink(srv1_proxy, s3, use_htb=True, params1={'quantum': 1500})
    net.addLink(srv1_web, s3, use_htb=True, params1={'quantum': 1500})
    net.addLink(srv1_video, s3, use_htb=True, params1={'quantum': 1500})
    
    # Server 2 internal network
    net.addLink(srv2_proxy, srv2_web, use_htb=True, params1={'quantum': 1500})
    net.addLink(srv2_proxy, srv2_video, use_htb=True, params1={'quantum': 1500})

    # Proxy public links
    net.addLink(srv1_proxy, s2, cls=TCLink, bw=500, delay="5ms", use_htb=True, params1={'quantum': 1500})
    net.addLink(srv2_proxy, s2, cls=TCLink, bw=500, delay="5ms", use_htb=True, params1={'quantum': 1500})

    net.addLink(r1, s2, cls=TCLink, bw=1000, delay="1ms", use_htb=True, params1={'quantum': 1500})

    info("*** Starting network\n")
    net.start()

    info("*** Configuring router\n")
    r1.cmd("sysctl -w net.ipv4.ip_forward=1")
    r1.cmd("ifconfig r1-eth0 10.0.0.254/24")
    r1.cmd("ifconfig r1-eth1 10.0.1.254/24")

    info("*** Configuring routes\n")
    h1.cmd("ip route add default via 10.0.0.254")
    h2.cmd("ip route add default via 10.0.0.254")
    srv1_proxy.cmd("ip route add default via 10.0.1.254")
    srv2_proxy.cmd("ip route add default via 10.0.1.254")
    
    # Assign IP addresses
    info("*** Configuring Server 1 internal network\n")

    # Enable IP forwarding on srv1-proxy
    srv1_proxy.cmd("sysctl -w net.ipv4.ip_forward=1")
    srv1_proxy.cmd("ifconfig srv1_proxy-eth1 192.168.1.1/24")
    srv1_web.cmd("ifconfig srv1_web-eth0 192.168.1.2/24")
    srv1_video.cmd("ifconfig srv1_video-eth0 192.168.1.3/24")

    # Set default routes
    srv1_web.cmd("ip route add default via 192.168.1.1")
    srv1_video.cmd("ip route add default via 192.168.1.1")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")

    # Register cleanup function to run on exit
    atexit.register(cleanup)

    parser = argparse.ArgumentParser(description='Mininet Topology for TCP and QUIC Testing')
    parser.add_argument('--bw_client', type=float, default=20, help='Bandwidth for client network in Mbps')
    parser.add_argument('--latency_client', type=str, default='10ms', help='Latency for client network')
    parser.add_argument('--region', type=str, choices=['India', 'Germany'], help='Region for client network settings')

    args = parser.parse_args()

    if args.region:
        if args.region == 'India':
            args.bw_client = 20
            args.latency_client = "80ms"
        elif args.region == 'Germany':
            args.bw_client = 500
            args.latency_client = "20ms"
    else: 
        args.bw_client = 20
        args.latency_client = "10ms"


    try:
        setup_network(bw_client=args.bw_client, latency_client=args.latency_client, region=args.region)
    except Exception as e:
        info(f"*** Error: {e}\n")
    finally:
        cleanup()
