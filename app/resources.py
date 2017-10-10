from uuid import uuid4
import webargs
from typing import Dict
from flask_restful import Resource, fields, marshal_with
from webargs.flaskparser import use_kwargs
from .blockchain import Blockchain

node_identifier = str(uuid4()).replace('-', '')


class Transaction(Resource):
    transaction_args = {
        'sender': webargs.fields.Str(required=True),
        'recipient': webargs.fields.Str(required=True),
        'amount': webargs.fields.Float(required=True)
    }

    def __init__(self, blockchain: Blockchain):
        self._blockchain = blockchain

    @use_kwargs(transaction_args)
    def post(self, sender: str, recipient: str, amount: float) -> (Dict, int):

        index = self._blockchain.new_transaction(sender, recipient, amount)

        return {
            'message': f'Transaction will be added to block {index}'
        }, 201


transaction_fields = {
    'sender': fields.String,
    'recipient': fields.String,
    'amount': fields.Float
}

block_fields = {
    'index': fields.Integer,
    'timestamp': fields.Float,
    'transactions': fields.List(fields.Nested(transaction_fields)),
    'proof': fields.Integer,
    'previous_hash': fields.String
}

chain_fields = {
    'length' : fields.Integer(default=0),
    'chain': fields.List(fields.Nested(block_fields), attribute='_chain')
}


class Chain(Resource):
    def __init__(self, blockchain: Blockchain):
        self._blockchain = blockchain

    @marshal_with(chain_fields)
    def get(self) -> Blockchain:
        return self._blockchain


mine_fields = {
    'message': fields.String,
    'index': fields.Integer(attribute='block.index'),
    'proof': fields.Float(attribute='block.proof'),
    'hash': fields.String(attribute='block.previous_hash'),
    'transactions': fields.List(fields.Nested(transaction_fields), attribute='block.transactions')
}


class Mine(Resource):
    def __init__(self, blockchain: Blockchain):
        self._blockchain = blockchain

    @marshal_with(mine_fields)
    def get(self) -> Dict:
        last_block = self._blockchain.last_block
        last_proof = last_block.proof
        proof = self._blockchain.proof_of_work(last_proof)

        self._blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)

        block = self._blockchain.new_block(proof)

        return {
            'message': 'New block forged',
            'block': block
        }