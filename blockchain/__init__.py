import hashlib
import json
from time import time
from typing import NamedTuple, List, Optional

__all__ = ['Blockchain']


class Transaction(NamedTuple):
    sender: str
    recipient: str
    amount: float

    def __repr__(self):
        return f'<Transaction {self.sender}:{self.recipient}>'


class Block(NamedTuple):
    index: int
    timestamp: float
    transactions: List[Transaction]
    proof: int
    previous_hash: Optional[str]

    def __repr__(self):
        return f'<Block {self.index}:{self.timestamp}>'


class Blockchain:
    def __init__(self):
        self._chain : List[Block] = []
        self._current_transactions: List[Transaction] = []

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

    def new_block(self, proof: int, previous_hash: Optional[str]) -> Block:
        block = Block(
            index=len(self._chain) + 1,
            timestamp=time(),
            transactions=self._current_transactions,
            proof=proof,
            previous_hash=previous_hash
        )

        self._current_transactions = []
        self._chain.append(block)

        return block

    @property
    def last_block(self) -> Optional(Block):
        if len(self._chain) == 0:
            return None
        return self._chain[-1]

    @staticmethod
    def hash(block) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[-4] == '0000'
