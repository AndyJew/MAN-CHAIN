
import hashlib
import json
import time


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
        }

        encoded = json.dumps(
            content,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(
            0,
            0,
            {"message": "MAN-CHAIN genesis block"},
            "0" * 64,
        )

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous = self.get_latest_block()

        block = Block(
            len(self.chain),
            int(time.time()),
            data,
            previous.hash,
        )

        self.chain.append(block)
        return block

    def is_valid(self):
        for i, block in enumerate(self.chain):
            if block.hash != block.calculate_hash():
                return False

            if i == 0:
                if block.previous_hash != "0" * 64:
                    return False
            else:
                previous = self.chain[i - 1]

                if block.previous_hash != previous.hash:
                    return False

                if block.index != previous.index + 1:
                    return False

        return True

    def to_dict(self):
        return {
            "name": "MAN-CHAIN",
            "version": 1,
            "blocks": [block.to_dict() for block in self.chain],
            "valid": self.is_valid(),
        }


if __name__ == "__main__":
    chain = Blockchain()

    chain.add_block({
        "type": "demo",
        "message": "First MAN-CHAIN transaction",
    })

    chain.add_block({
        "type": "demo",
        "message": "Second MAN-CHAIN transaction",
    })

    print(json.dumps(
        chain.to_dict(),
        indent=2,
        ensure_ascii=False,
    ))
