import hashlib
import time
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Decentralized security tool controller prototype
class SecurityToolController:
    def __init__(self):
        self.nodes = set()
        self.blockchain = []

    def add_node(self, node):
        self.nodes.add(node)

    def get_nodes(self):
        return list(self.nodes)

    def create_block(self, data):
        previous_block = self.blockchain[-1] if self.blockchain else None
        if previous_block:
            previous_block_hash = hashlib.sha256(str(previous_block).encode()).hexdigest()
        else:
            previous_block_hash = None
        block = {
            'index': len(self.blockchain) + 1,
            'timestamp': time.time(),
            'data': data,
            'previous_block_hash': previous_block_hash
        }
        self.blockchain.append(block)
        return block

    def get_blockchain(self):
        return self.blockchain

    def create_transaction(self, sender, recipient, data):
        return {
            'sender': sender,
            'recipient': recipient,
            'data': data,
            'timestamp': time.time()
        }

    def broadcast_transaction(self, transaction):
        for node in self.nodes:
            requests.post(f'http://{node}/add_transaction', json=transaction)

    def verify_chain(self):
        for i in range(1, len(self.blockchain)):
            current_block = self.blockchain[i]
            previous_block = self.blockchain[i - 1]
            if current_block['previous_block_hash'] != hashlib.sha256(str(previous_block).encode()).hexdigest():
                return False
        return True

controller = SecurityToolController()

@app.route('/add_node', methods=['POST'])
def add_node():
    node = request.json['node']
    controller.add_node(node)
    return jsonify({'message': f'Node added: {node}'})

@app.route('/get_nodes', methods=['GET'])
def get_nodes():
    return jsonify({'nodes': controller.get_nodes()})

@app.route('/create_block', methods=['POST'])
def create_block():
    data = request.json['data']
    block = controller.create_block(data)
    return jsonify({'block': block})

@app.route('/get_blockchain', methods=['GET'])
def get_blockchain():
    return jsonify({'blockchain': controller.get_blockchain()})

@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    sender = request.json['sender']
    recipient = request.json['recipient']
    data = request.json['data']
    transaction = controller.create_transaction(sender, recipient, data)
    controller.broadcast_transaction(transaction)
    return jsonify({'transaction': transaction})

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transaction = request.json
    # TO DO: implement transaction verification
    controller.create_block(transaction)
    return jsonify({'message': 'Transaction added'})

if __name__ == '__main__':
    app.run(debug=True)