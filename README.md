# MyBlockchain
## 📖 Description
MyBlockchain is a simple blockchain implementation in Python. This project uses basic concepts of security and data structures to create, store, and verify linked blocks. Key features include:

Adding new blocks.
Searching for blocks by index or hash.
Validating the blockchain's integrity.
Saving and loading the blockchain state from a binary file.


## 🚀 Features

Add new blocks: Create entries in the blockchain with custom data.
Search blocks: Find blocks by index or hash.
Display blockchain: View all blocks and their details.
Validate blockchain: Ensure the integrity of the entire chain.
Persistence: The blockchain is automatically saved and loaded from a binary file (blockchain.bin).


## 📂 Project Structure
```
MyBlockchain/
├── MyBlockchain.py         # Main code
├── blockchain.bin        # BlockChain Binary File
├── requirements.txt      # Requirements to Run the Project
├── README.md             # Project documentation
```


## 🛠️ How to Run the Project
### 1. Prerequisites
Ensure Python (3.8 or later) is installed on your system. It's not necessary to install any external libraries, as the code uses only Python's built-in modules.
### 2. Run the program
Simply execute the script:
```bash
python MyBlockchain.py
```


## 📋 Menu Options
When you run the program, you'll see the following interactive menu:
```
┌────────────────────────────────────────┐
│           🌌 MY BLOCKCHAIN 🌌          │
├────────────────────────────────────────┤
│ [1] 🚀 New BlockChain Entry            │
│ [2] 🔍 Find Block                      │
│ [3] 📜 Show BlockChain                 │
│ [4] ✅ BlockChain Validation           │
│ [5] 🌐 Start HTTP Server [OFF]         │
│ [6] ❌ Exit                            │
└────────────────────────────────────────┘
```
### Main Features

New BlockChain Entry: Add a new block with custom information.
Find Block: Search blocks by index or hash.
Show BlockChain: List all blocks in the blockchain.
BlockChain Validation: Validate the integrity of the blockchain.
BlockChain API: Run a HTTP Server to access and insert blocks via API.
Exit: Save the blockchain and exit the program.


## 💾 Data Persistence

The blockchain data is stored in the blockchain.bin file using Python's pickle module.
The blockchain is automatically loaded when the program starts and saved when a new block is added or the program exits.


## 🔍 Data Structure
### Block Class
Represents each block in the blockchain.
```
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Calculates the hash using SHA-256
```
### Blockchain Class
Manages the chain of blocks.
```
class Blockchain:
    def __init__(self):
        self.index = 0
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Creates the initial block
```

## ✅ Blockchain Validation
The is_valid method ensures:

The hash of each block is correct.
Each block’s previous_hash matches the hash of the previous block.


## 🛠️ Tools Used

Python 3.x (No external libraries required)
Hashlib: For secure SHA-256 hash generation.
Pickle: To save and load the blockchain in binary format.


## 📜 License
This project is available under the MIT License. Feel free to use, modify, and distribute it as needed.

This README ensures that developers can understand and quickly start using MyBlockchain! 🎉
