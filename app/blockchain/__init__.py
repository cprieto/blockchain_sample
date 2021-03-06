import hashlib
import jsonpickle
from time import time
from typing import List, Optional
from urllib.parse import urlparse

__all__ = ['Blockchain']


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender: str = sender
        self.recipient: str = recipient
        self.amount: float = amount

    def __repr__(self):
        return f'<Transaction {self.sender}:{self.recipient}>'


class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Transaction], proof: int, previous_hash: str):
        self.index: int = index
        self.timestamp: float = timestamp
        self.transactions: List[Transaction] = transactions
        self.proof: int = proof
        self.previous_hash: Optional[str] = previous_hash

    def __repr__(self):
        return f'<Block {self.index}:{self.timestamp}>'


class Blockchain:
    def __init__(self):
        self._chain: List[Block] = []
        self._current_transactions: List[Transaction] = []
        self.nodes = set()

        self.new_block(proof=100, previous_hash=None)

    def new_transaction(self, sender: str, recipient: str, amount: float) -> int:
        self._current_transactions.append(Transaction(
            sender=sender,
            recipient=recipient,
            amount=amount
        ))

        if self.last_block:
            return self.last_block.index + 1
        return 1

    def register_node(self, address: str):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_block(self, proof: int, previous_hash: Optional[str] = None) -> Block:

        block = Block(
            index=len(self._chain) + 1,
            timestamp=time(),
            transactions=self._current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.hash(self.last_block)
        )

        self._current_transactions = []
        self._chain.append(block)

        return block

    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @property
    def length(self) -> int:
        return len(self._chain)

    @property
    def last_block(self) -> Optional[Block]:
        if len(self._chain) == 0:
            return None
        return self._chain[-1]

    @staticmethod
    def hash(block: Optional[Block]) -> str:
        if not block:
            return ''

        block_string = jsonpickle.dumps(block.__dict__, unpicklable=False).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    @staticmethod
    def valid_chain(chain: List[Block]):
        if len(chain) == 0:
            return True

        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block.previous_hash != Blockchain.hash(last_block):
                return False
            if not Blockchain.valid_proof(last_block.proof, block.proof):
                return False

            last_block = block
            current_index += 1
        return True
