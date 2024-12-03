#!/usr/bin/env python
import os

from mininet.net import Containernet
from mininet.node import Controller, Docker
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def setup_network(bw_client=20, latency_client="10ms"):
    net = Containernet(controller=Controller)

    info("*** Adding controller\n")
    net.addController("c0")

    info("*** Adding switches\n")
    s1 = net.addSwitch("s1")  # Client switch
    s2 = net.addSwitch("s2")  # Server switch

    info("*** Adding router\n")
    r1 = net.addHost("r1", ip="10.0.0.254")

    info("*** Adding clients\n")
    h1 = net.addDocker("h1", ip="10.0.0.1/24", dimage="host-web-image", volumes=[f"{os.getcwd()}/../stats/assets/pcaps:/pcaps:rw"]) #, dcmd="/bin/bash ./curl_request.sh")
    h2 = net.addDocker("h2", ip="10.0.0.2/24", dimage="host-image")

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
    srv1_web = net.addDocker("srv1-web", ip="192.168.1.2/24", dimage="web-server-image")
    srv1_video = net.addDocker("srv1-video", ip="192.168.1.3/24", dimage="video-server-image")

    # Server 2
    srv2_proxy = net.addDocker(
        "srv2-proxy",
        ip="10.0.1.2/24",
        dimage="proxy-server-image",
        ports=[443],
        port_bindings={443: 9443},
        dcmd="caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"
    )
    srv2_web = net.addDocker("srv2-web", ip="192.168.2.2/24", dimage="web-server-image")
    srv2_video = net.addDocker("srv2-video", ip="192.168.2.3/24", dimage="video-server-image")

    info("*** Creating links\n")

    # Client links
    net.addLink(h1, s1, cls=TCLink, bw=bw_client, delay=latency_client)
    net.addLink(h2, s1, cls=TCLink, bw=bw_client, delay=latency_client)
    net.addLink(s1, r1, cls=TCLink, bw=bw_client, delay=latency_client)

    # Server 1 internal network
    net.addLink(srv1_proxy, srv1_web)
    net.addLink(srv1_proxy, srv1_video)

    # Server 2 internal network
    net.addLink(srv2_proxy, srv2_web)
    net.addLink(srv2_proxy, srv2_video)

    # Proxy public links
    net.addLink(srv1_proxy, s2, cls=TCLink, bw=500, delay="5ms")
    net.addLink(srv2_proxy, s2, cls=TCLink, bw=500, delay="5ms")

    net.addLink(r1, s2, cls=TCLink, bw=1000, delay="1ms")

    info("*** Starting network\n")
    net.start()

    info("*** Configuring router\n")
    r1.cmd("sysctl -w net.ipv4.ip_forward=1")
    r1.cmd("ifconfig r1-eth0 10.0.0.254/24")
    r1.cmd("ifconfig r1-eth1 10.0.1.254/24")
    # r1.cmd("ifconfig r1-eth1 10.0.2.254/24")

    info("*** Configuring routes\n")
    h1.cmd("ip route add default via 10.0.0.254")
    h2.cmd("ip route add default via 10.0.0.254")
    srv1_proxy.cmd("ip route add default via 10.0.1.254")
    srv2_proxy.cmd("ip route add default via 10.0.1.254")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    setup_network()
