import hashlib
import pickle
import datetime as date

#EXEMPLOS DE DADOS A SALVAR
log_load = {
    'Log': 'Blockchain Loaded',   
}

log_save = {
    'Log': 'Blockchain Saved'  
}


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

def save_blockchain(blockchain, filename="blockchain.bin"):
    try:
        blockchain.add_block(Block(blockchain.index, date.datetime.now(), log_save, blockchain.chain[-1].hash))
        with open(filename, "wb") as file:
            pickle.dump(blockchain.chain, file)
        print("✅ Blockchain Saved!")
    except Exception as e:
        print(f"❌ Error saving blockchain: {e}")

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
    
def display_menu():
    print("┌────────────────────────────────────────┐")
    print("│           🌌 MY BLOCKCHAIN 🌌          │")
    print("├────────────────────────────────────────┤")
    print("│ [1] 🚀 New BlockChain Entry            │")
    print("│ [2] 🔍 Find Block                      │")
    print("│ [3] 📜 Show BlockChain                 │")
    print("│ [4] ✅  BlockChain Validation           │")
    print("│ [5] ❌  Exit                            │")
    print("└────────────────────────────────────────┘")



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




class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()
    
class Blockchain:
    def __init__(self):
        self.index = 0
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        genesis = Block(self.index, date.datetime.now(), 'Genesis Block', '0')
        self.index += 1
        return genesis

    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        self.index += 1

    def get_block(self, block_id):
        for block in self.chain:
            if block.index == block_id:
                print_block(block)
                return
            
        print("Block not found")
        return

    def get_hash(self, block_hash):
        for block in self.chain:
            if block.hash == block_hash:
                print_block(block)
                return
        print("Hash not found")
        return


    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True
    
    def save(self):
        save_blockchain(self)
    

my_blockchain = load_blockchain()


#my_blockchain.add_block(Block(my_blockchain.index, date.datetime.now(), compra1, my_blockchain.chain[-1].hash))
#my_blockchain.add_block(Block(my_blockchain.index, date.datetime.now(), doc, my_blockchain.chain[-1].hash))

print("Blockchain Integrity:", str(my_blockchain.is_valid()))
#print_blockchain(my_blockchain.chain)

while True:
    display_menu()
    option = int(input('>> '))
    print((20*'====='))

    try:
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
            print(f'BlockChain Integrity: {my_blockchain.is_valid()}')
            print((20*'====='))
            my_blockchain.save()
            print("Closing Blockchain manager...")
            break

        else:
            raise ValueError
    except ValueError:
        print("Try Again!")
        continue
            
