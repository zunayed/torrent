import unittest

from torrent import Torrent


class TestTorrentModel(unittest.TestCase):

    def setUp(self):
        self.torrent = Torrent('ub.torrent')

    def test_generate_peer_id(self):
        self.assertEqual(4, 4)
        pass

    def test_build_tracker_params(self):
        self.assertEqual(self.torrent.tracker_params['info_hash'],'\xcb\x84\xcc\xc1\x0f)m\xf7-l@\xbaz\x07\xc1x\xa42:\x14')
        self.assertEqual(self.torrent.tracker_params['port'],8123)
        self.assertEqual(self.torrent.tracker_params['uploaded'],0)
        self.assertEqual(self.torrent.tracker_params['downloaded'],0)
        self.assertEqual(self.torrent.tracker_params['left'],1028653056)
        self.assertEqual(self.torrent.tracker_params['compact'],1)
        self.assertEqual(self.torrent.tracker_params['no_peer_id'],0)
        self.assertEqual(len(self.torrent.tracker_params['peer_id']), 20)

    def test_announce_url(self):
        self.assertEqual(self.torrent.announce_url, 'http://torrent.ubuntu.com:6969/announce')

    def test_get_peer_list(self):
        expected_peer_list = ['31.16.170.106:6882', '213.89.96.185:6941', '50.173.173.26:48838', '85.239.121.202:51413', '146.115.161.94:51413', '37.187.17.222:51413', '2.224.179.235:25287', '62.210.236.9:51413', '5.135.186.165:6984', '177.182.204.16:46714', '81.90.237.124:666', '84.236.19.85:51999', '108.61.191.94:58869', '185.44.107.109:51413', '5.45.109.115:51413', '198.100.147.91:51103', '123.198.9.83:51413', '188.226.241.51:51413', '80.217.52.181:58882', '130.243.184.10:13350', '89.143.230.17:58826', '85.224.46.172:24366', '89.142.59.154:6884', '46.188.29.249:24261', '185.21.216.192:58153', '208.53.164.19:49325', '85.229.24.145:51412', '95.211.186.115:53076', '80.198.252.120:42000', '60.241.41.178:51413', '68.114.213.208:53281', '89.12.44.117:51413', '124.33.156.230:6890', '71.179.85.145:58090', '37.59.36.217:61050', '80.99.91.28:51413', '93.180.52.136:51413', '67.189.24.160:5555', '110.4.196.166:51413', '46.146.228.7:6866', '89.169.1.240:30254', '67.189.24.160:5555', '71.213.10.242:51413', '177.204.35.11:51413', '85.183.40.67:42478', '82.211.208.148:39249', '23.255.227.142:51413', '94.23.38.99:51103', '176.31.66.69:64305', '31.38.100.198:51413']
        self.torrent.tracker_response['peers'] = '\x1f\x10\xaaj\x1a\xe2\xd5Y`\xb9\x1b\x1d2\xad\xad\x1a\xbe\xc6U\xefy\xca\xc8\xd5\x92s\xa1^\xc8\xd5%\xbb\x11\xde\xc8\xd5\x02\xe0\xb3\xebb\xc7>\xd2\xec\t\xc8\xd5\x05\x87\xba\xa5\x1bH\xb1\xb6\xcc\x10\xb6zQZ\xed|\x02\x9aT\xec\x13U\xcb\x1fl=\xbf^\xe5\xf5\xb9,km\xc8\xd5\x05-ms\xc8\xd5\xc6d\x93[\xc7\x9f{\xc6\tS\xc8\xd5\xbc\xe2\xf13\xc8\xd5P\xd94\xb5\xe6\x02\x82\xf3\xb8\n4&Y\x8f\xe6\x11\xe5\xcaU\xe0.\xac_.Y\x8e;\x9a\x1a\xe4.\xbc\x1d\xf9^\xc5\xb9\x15\xd8\xc0\xe3)\xd05\xa4\x13\xc0\xadU\xe5\x18\x91\xc8\xd4_\xd3\xbas\xcfTP\xc6\xfcx\xa4\x10<\xf1)\xb2\xc8\xd5Dr\xd5\xd0\xd0!Y\x0c,u\xc8\xd5|!\x9c\xe6\x1a\xeaG\xb3U\x91\xe2\xea%;$\xd9\xeezPc[\x1c\xc8\xd5]\xb44\x88\xc8\xd5C\xbd\x18\xa0\x15\xb3n\x04\xc4\xa6\xc8\xd5.\x92\xe4\x07\x1a\xd2Y\xa9\x01\xf0v.C\xbd\x18\xa0\x15\xb3G\xd5\n\xf2\xc8\xd5\xb1\xcc#\x0b\xc8\xd5U\xb7(C\xa5\xeeR\xd3\xd0\x94\x99Q\x17\xff\xe3\x8e\xc8\xd5^\x17&c\xc7\x9f\xb0\x1fBE\xfb1\x1f&d\xc6\xc8\xd5'
        peer_list = self.torrent.get_peer_list()
        for expected_peer in expected_peer_list:
            self.assertIn(expected_peer, peer_list)

    def test_get_handshake(self):
        pass



if __name__ == '__main__':
    unittest.main()
