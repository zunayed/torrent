import requests
import hashlib
import random
import string
import socket
import struct

from bencode import bencode, bdecode

with open("ub.torrent") as f:
    decoded_data = bdecode(f.read())

announce_url = decoded_data['announce']
info = decoded_data['info']
info_hash = hashlib.sha1(bencode(info)).digest()

peer_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))

uploaded = 0
downloaded = 0

overall_file_length = info['length']
left = overall_file_length

compact = 1
no_peer_id = 0

port = 8000

tracker_params = {
    'info_hash': info_hash,
    'peer_id': peer_id,
    'port': port,
    'uploaded': uploaded,
    'downloaded': downloaded,
    'left': left,
    'compact': compact,
    'no_peer_id': no_peer_id,
}

response = requests.get(announce_url, params=tracker_params)
response_decoded = bdecode(response.content)
peers = response_decoded['peers']

peer_address = ''
peer_list = []

print "%r" % peers

for i, peer in enumerate(peers):
#    import ipdb
#    ipdb.set_trace()
#    print i, peer
#    print ord(peer)
    if i % 6 == 4:
        port_large = ord(peer) * 256
    elif i % 6 == 5:
        port = port_large + ord(peer)
        peer_address += ':' + str(port)
        peer_list.append(peer_address)
        peer_address = ''
    elif i % 6 == 3:
        peer_address += str(ord(peer))
    else:
        peer_address += str(ord(peer)) + '.'

print "Peer List: %r", peer_list[0]
peer_full_add = peer_list[0].split(':')
peer_ip_address = peer_full_add[0]
peer_port = int(peer_full_add[1])

sock = socket.socket()
sock.connect((peer_ip_address,peer_port))

# handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
pstrlen = 19
pstr = "BitTorrent protocol"
reserved = "\x00"*8
hs_info_hash = info_hash
hs_peer_id = peer_id

handshake = str(pstrlen) + pstr + reserved + hs_info_hash + hs_peer_id

#test2 = struct.pack('bsqss',pstrlen,pstr,reserved,hs_info_hash,hs_peer_id)

print handshake

import ipdb
ipdb.set_trace()



