import hashlib
import pickle
import datetime as date
from flask import Flask, jsonify, request
from threading import Thread
import logging
import time

#GLOBAL
#HTTP SERVER SETTINGS
app = Flask(__name__) # Instance of the Flask Server
server_status = False # Save the server status to verify if it was started
server_thread = None # Save the Server Thread in the variable
server_port = 5000 # Change to any preferred port
host_global = False # Set True for WAN and False for LAN Only

logging.basicConfig(filename='flask.log', level=logging.INFO) # Save HTTP Server logs in flask.log

#EXAMPLES OF DATA TO SAVE
log_load = {
    'Log': 'Blockchain Loaded',   
}

log_save = {
    'Log': 'Blockchain Saved'  
}

#FUNCTIONS TO DEAL WITH THE FLASK SERVER TO SERVE THE API5
def run_flask_server():
    global server_status
    if server_status == False:
        if host_global == False:
            app.run(host='127.0.0.1', port=server_port, debug=False, use_reloader=False, threaded=True) # Start Server on LAN Only
        else:
            app.run(host='0.0.0.0', port=server_port, debug=False, use_reloader=False, threaded=True) # Start Server on WAN
        server_status = True
    



def run_http_server():
    global server_status, server_thread
    if server_status:
        print("🚀 HTTP Server is already running!")
        return
    print("🚀 Starting HTTP Server...")
    server_thread = Thread(target=run_flask_server, daemon=True)
    server_thread.start()
    time.sleep(2)
    print("🚀 HTTP Server is running!...")
    return

def http_status():
    if server_status:
        return "ON "
    else:
        return "OFF"

#FUNCTIONS TO DEAL WITH THE API
@app.route('/')
def home():
    return 'Welcome to the MyBlockchain API!'

# Route: Get all blocks
@app.route('/blocks', methods=['GET'])
def get_blocks():
    return jsonify([{
        'index': block.index,
        'timestamp': block.timestamp.isoformat(),
        'data': block.data,
        'previous_hash': block.previous_hash,
        'hash': block.hash
    } for block in my_blockchain.chain])

# Route: Add a new block
@app.route('/blocks', methods=['POST'])
def add_block():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'Data is required'}), 400

    new_block = Block(my_blockchain.index, date.datetime.now(), data, my_blockchain.chain[-1].hash)
    my_blockchain.add_block(new_block)
    my_blockchain.save()
    return jsonify({
        'message': 'Block added successfully!',
        'block': {
            'index': new_block.index,
            'timestamp': new_block.timestamp.isoformat(),
            'data': new_block.data,
            'previous_hash': new_block.previous_hash,
            'hash': new_block.hash
        }
    }), 201

# Route: Get block by index
@app.route('/blocks/<int:index>', methods=['GET'])
def get_block_by_index(index):
    for block in my_blockchain.chain:
        if block.index == index:
            return jsonify({
                'index': block.index,
                'timestamp': block.timestamp.isoformat(),
                'data': block.data,
                'previous_hash': block.previous_hash,
                'hash': block.hash
            })
    return jsonify({'error': 'Block not found'}), 404

# Route: Get block by hash
@app.route('/blocks/hash/<hash>', methods=['GET'])
def get_block_by_hash(hash):
    for block in my_blockchain.chain:
        if block.hash == hash:
            return jsonify({
                'index': block.index,
                'timestamp': block.timestamp.isoformat(),
                'data': block.data,
                'previous_hash': block.previous_hash,
                'hash': block.hash
            })
    return jsonify({'error': 'Block not found'}), 404

# Route: Validate the blockchain
@app.route('/validate', methods=['GET'])
def validate_blockchain():
    is_valid = my_blockchain.is_valid()
    return jsonify({'valid': is_valid})



#CONSOLE PRINT FUNCTIONS
#   PRINT ALL BLOCKS IN THE BLOCKCHAIN
def print_blockchain(chain):
    for block in chain:
        print("╔"+ 27*"═══")
        print(f"║ 📦 BLOCK {block.index} ({block.hash})        ")
        print("╠", 27*"═══")
        print(f"║ Block Index   : {block.index}")
        print(f"║ Timestamp     : {block.timestamp}")
        print(f"║ Data          : {block.data}")
        print(f"║ Previous Hash : {block.previous_hash}   ")
        print(f"║ Hash          : {block.hash}   ")
        print("╚"+ 27*"═══")
        print(20*'-----')
    print((20*'====='))

#   PRINT SPECIFIC BLOCK FROM BLOCKCHAIN
def print_block(block):
    print("╔"+ 27*"═══")
    print(f"║ 📦 BLOCK {block.index} ({block.hash})        ")
    print("╠", 27*"═══")
    print(f"║ Block Index   : {block.index}")
    print(f"║ Timestamp     : {block.timestamp}")
    print(f"║ Data          : {block.data}")
    print(f"║ Previous Hash : {block.previous_hash}   ")
    print(f"║ Hash          : {block.hash}   ")
    print("╚"+ 27*"═══")
    print(20*'-----')
    print((20*'====='))

#FUNCTIONS TO DEAL WITH BINARY FILE OF BLOCKCHAIN
#   FUNCTION TO SAVE THE BLOCKCHAIN FILE
def save_blockchain(blockchain, filename="blockchain.bin"):
    try:
        blockchain.add_block(Block(blockchain.index, date.datetime.now(), log_save, blockchain.chain[-1].hash))
        with open(filename, "wb") as file:
            pickle.dump(blockchain.chain, file)
        print("✅ Blockchain Saved!")
    except Exception as e:
        print(f"❌ Error saving blockchain: {e}")

#   FUNCTION TO LOAD THE BLOCKCHAIN FILE IN THE PROGRAM
def load_blockchain(filename="blockchain.bin"):
    try:
        with open(filename, "rb") as file:
            chain = pickle.load(file)
            blockchain = Blockchain()
            blockchain.chain = chain
            blockchain.index = len(chain)
        blockchain.add_block(Block(blockchain.index, date.datetime.now(), log_load, blockchain.chain[-1].hash))
        print("✅ Blockchain Loaded!")
        return blockchain
    
    except FileNotFoundError:
        print("⚠️ Blockchain file not found. Creating new blockchain")
        return Blockchain()
    except Exception as e:
        print(f"❌ Error when loading blockchain: {e}")
        return Blockchain()

#MENUS
#   FUNCTION TO PRINT THE MAIN MENU
def display_menu():
    print("┌────────────────────────────────────────┐")
    print("│           🌌 MY BLOCKCHAIN 🌌          │")
    print("├────────────────────────────────────────┤")
    print("│ [1] 🚀 New BlockChain Entry            │")
    print("│ [2] 🔍 Find Block                      │")
    print("│ [3] 📜 Show BlockChain                 │")
    print("│ [4] ✅  BlockChain Validation          │")
    print(f"│ [5] 🌐 Start HTTP Server [{http_status()}]         │")
    print("│ [6] ❌  Exit                           │")
    print("└────────────────────────────────────────┘")


#   OPEN THE MENU TO FIND A SPECIFIC BLOCK
def find_block_menu():
    while True:
        print("┌────────────────────────────────────────┐")
        print("│           🔍 BLOCK SEARCH 🔍           │")
        print("├────────────────────────────────────────┤")
        print("│ [1] 🔍 Search by Index                 │")
        print("│ [2] 🔍 Search by Hash                  │")
        print("│ [3]  ↩ Return to Main Menu             │")
        print("└────────────────────────────────────────┘")
        option = int(input(">> "))

        try:
            if option == 1:
                index = int(input("Block Index: "))
                print((20*'====='))
                my_blockchain.get_block(index)
                continue
            elif option == 2:
                hash = input("Block Hash: ")
                print((20*'====='))
                my_blockchain.get_hash(hash)
                continue
            elif option == 3:
                return
            else:
                return ValueError

        except ValueError:
            print("Try Again.")
            continue



#OBJECTS
#   OBJECT BLOCK
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    #CALCULATE THE SHA256 HASH OF THE BLOCK 
    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

#   OBJECT BLOCKCHAIN
class Blockchain:
    def __init__(self):
        self.index = 0
        self.chain = [self.create_genesis_block()]

    # FUNCTION TO CREATE THE GENESIS BLOCK WHEN INITIALIZE A NEW BLOCKCHAIN OBJECT
    def create_genesis_block(self):
        genesis = Block(self.index, date.datetime.now(), 'Genesis Block', '0')
        self.index += 1
        return genesis

    # FUNCTION TO ADD A NEW BLOCK IN THE END OF THE BLOCKCHAIN OBJECT
    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        self.index += 1

    # FUNCTION TO GET A BLOCK BY ID/INDEX
    def get_block(self, block_id):
        for block in self.chain:
            if block.index == block_id:
                print_block(block)
                return
            
        print("Block not found")
        return

    # FUNCTION TO GET A BLOCK BY HASH
    def get_hash(self, block_hash):
        for block in self.chain:
            if block.hash == block_hash:
                print_block(block)
                return
        print("Hash not found")
        return

    # FUNCTION THAT CHECKS IF THE BLOCKCHAIN IS VALID
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True
    
    # FUNCTION TO SAVE THE BLOCKCHAIN OBJECT IN THE BINARY FILE
    def save(self):
        save_blockchain(self)
    
# LOAD BLOCKCHAIN BINARY FILE
my_blockchain = load_blockchain()

# EXAMPLE TO ADD NEW BLOCKS IN THE BLOCKCHAIN
#my_blockchain.add_block(Block(my_blockchain.index, date.datetime.now(), DATA1, my_blockchain.chain[-1].hash))
#my_blockchain.add_block(Block(my_blockchain.index, date.datetime.now(), DATA2, my_blockchain.chain[-1].hash))

# PRINT THE INTEGRITY OF THE LOADED BLOCKCHAIN
print("Blockchain Integrity:", str(my_blockchain.is_valid()))

while True:
    display_menu()
    try:
        option = int(input('>> '))
        print((20*'====='))

        if option == 1:
            data = input("Data to be added in the blockchain: ")
            my_blockchain.add_block(Block(my_blockchain.index, date.datetime.now(), data, my_blockchain.chain[-1].hash))
            print('')
            my_blockchain.get_block(my_blockchain.index - 1)
            print('')
            print(f'BlockChain Integrity: {my_blockchain.is_valid()}')
            print((20*'====='))
            if my_blockchain.is_valid():
                my_blockchain.save()

        elif option == 2:
            find_block_menu()
            continue

        elif option == 3:
            print_blockchain(my_blockchain.chain)
            continue

        elif option == 4:
            print(f'BlockChain Integrity: {my_blockchain.is_valid()}')
            print((20*'====='))
            continue

        elif option == 5:
            run_http_server()
            continue
        elif option == 6:
            print(f'BlockChain Integrity: {my_blockchain.is_valid()}')
            print((20*'====='))
            my_blockchain.save()
            print("Closing Blockchain manager...")
            break

        else:
            raise ValueError("Invalid Option. Try Again")
    except ValueError as e:
        print("Try Again!")
        continue
            
