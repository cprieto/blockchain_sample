from typing import Dict
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_kwargs
from .blockchain import Blockchain


class Transaction(Resource):
    transaction_args = {
        'sender': fields.Str(required=True),
        'recipient': fields.Str(required=True),
        'amount': fields.Float(required=True)
    }

    def __init__(self, blockchain: Blockchain):
        self._blockchain = blockchain

    @use_kwargs(transaction_args)
    def post(self, sender: str, recipient: str, amount: float) -> Dict:

        index = self._blockchain.new_transaction(sender, recipient, amount)

        return {
            'message': f'I create a transaction boy, with index {index}',
            'index': index
        }

