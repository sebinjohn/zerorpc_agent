import socket
import argparse
import zerorpc

parser = argparse.ArgumentParser(description='Firewall Test agent arguments')
parser.add_argument("host",
                    help='hostname of the machine in which it is running')
# parser.add_argument("server_url", help='URL of the server hosting the rules')
args = parser.parse_args()


def test_connectivity(dest_ip, port, proto):
    if(proto == "TCP"):
        proto_type = socket.SOCK_STREAM
    elif(proto == "UDP"):
        proto_type = socket.SOCK_DGRAM

    sock = socket.socket(socket.AF_INET, proto_type)
    status = sock.connect_ex((dest_ip, port))
    sock.close()
    print str(dest_ip) + " : " + str(port) + " : " + proto + " : " + str(status)
    return status


class KickBackServer(object):
    def get_firewall_status(self, destination_ip, port, protocol):
        print destination_ip, port
        status = test_connectivity(destination_ip, port, protocol)
        # dict connection_status = {
        #     'source': args.host,
        #     'destination': destination_ip,
        #     'destination_port': port,
        #     'protocol': protocol,
        #     'status': status
        # }
        # return connection_status
        return status

s = zerorpc.Server(KickBackServer())
s.bind('tcp://0.0.0.0:4242')
s.run()
