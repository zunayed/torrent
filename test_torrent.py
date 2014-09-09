import unittest

from torrent import Torrent


class TestTorrentModel(unittest.TestCase):

    def setUp(self):
        self.torrent = Torrent('ub.torrent')

    def test_generate_peer_id(self):
        self.assertEqual(4, 4)
        pass

    def test_build_tracker_params(self):
        pass

    def test_get_peer_list(self):
        pass

    def test_get_handshake(self):
        pass


if __name__ == '__main__':
    unittest.main()
