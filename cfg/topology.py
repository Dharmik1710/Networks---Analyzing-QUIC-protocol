#!/usr/bin/env python

import argparse
from mininet.net import Containernet
from mininet.node import Controller, Docker, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def setup_network(bw_client=20, latency_client='10ms'):
    net = Containernet(controller=Controller)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    info('*** Adding router\n')
    r1 = net.addHost('r1', ip='0.0.0.0')

    info('*** Adding hosts (clients)\n')
    h1 = net.addDocker('h1', ip='10.0.0.1/24', dimage="host-image")
    h2 = net.addDocker('h2', ip='10.0.0.2/24', dimage="host-image")

    info('*** Adding servers\n')
    srv1 = net.addDocker('srv1', ip='10.0.1.1/24', dimage="server-image")
    srv2 = net.addDocker('srv2', ip='10.0.1.2/24', dimage="server-image")

    info('*** Creating links\n')

    # Client network links with bandwidth and latency constraints
    net.addLink(h1, s1, cls=TCLink, bw=bw_client, delay=latency_client)
    net.addLink(h2, s1, cls=TCLink, bw=bw_client, delay=latency_client)
    net.addLink(s1, r1, cls=TCLink, bw=bw_client, delay=latency_client)

    # Server network links
    net.addLink(srv1, s2)
    net.addLink(srv2, s2)
    net.addLink(r1, s2, cls=TCLink, bw=500, delay='5ms')

    info('*** Starting network\n')
    net.start()

    info('*** Configuring router interfaces\n')
    r1.cmd('ifconfig r1-eth0 10.0.0.254/24')  # Interface towards clients
    r1.cmd('ifconfig r1-eth1 10.0.1.254/24')  # Interface towards servers

    info('*** Setting up IP forwarding on router\n')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Configuring default routes\n')
    h1.cmd('ip route add default via 10.0.0.254')
    h2.cmd('ip route add default via 10.0.0.254')
    srv1.cmd('ip route add default via 10.0.1.254')
    srv2.cmd('ip route add default via 10.0.1.254')

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    parser = argparse.ArgumentParser(description='Mininet Topology for TCP and QUIC Testing')
    parser.add_argument('--bw_client', type=float, default=20, help='Bandwidth for client network in Mbps')
    parser.add_argument('--latency_client', type=str, default='10ms', help='Latency for client network')
    args = parser.parse_args()
    setup_network(bw_client=args.bw_client, latency_client=args.latency_client)
