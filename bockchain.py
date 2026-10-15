
import unittest

from blockchain import Blockchain


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.chain = Blockchain()

    def test_genesis_block_exists(self):
        self.assertEqual(len(self.chain.chain), 1)
        self.assertTrue(self.chain.is_valid())

    def test_add_block(self):
        block = self.chain.add_block({
            "type": "demo",
            "message": "Hello MAN-CHAIN",
        })

        self.assertEqual(block.index, 1)
        self.assertEqual(len(self.chain.chain), 2)
        self.assertTrue(self.chain.is_valid())

    def test_blocks_are_linked(self):
        first = self.chain.add_block({"amount": 10})
        second = self.chain.add_block({"amount": 20})

        self.assertEqual(
            second.previous_hash,
            first.hash,
        )
        self.assertTrue(self.chain.is_valid())

    def test_detect_modified_data(self):
        self.chain.add_block({"amount": 10})

        self.chain.chain[1].data["amount"] = 999

        self.assertFalse(self.chain.is_valid())

    def test_detect_broken_link(self):
        self.chain.add_block({"amount": 10})
        self.chain.add_block({"amount": 20})

        self.chain.chain[2].previous_hash = "broken"

        self.assertFalse(self.chain.is_valid())


if __name__ == "__main__":
    unittest.main()
