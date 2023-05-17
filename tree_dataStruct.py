class nodeHuff:
    def __init__(self, freq:int, symbol:str, left=None, right=None):
        # frequency of symbol
        self.freq = freq
 
        # symbol name (character)
        self.symbol = symbol
 
        # node left of current node
        self.left = left
 
        # node right of current node
        self.right = right
 
        # tree direction (0/1)
        self.huff = ''
         
    def __lt__(self, nxt):
        return self.freq < nxt.freq

class Node:
    
    def __init__(self, data:str):
        self.left = None
        self.right = None
        self.data = data
      
    def isLeaf(self) -> bool:
        return (self.right == None and self.left == None)
    
    def next(self, data:str):
        if      data == '0': return self.left
        elif    data == '1': return self.right
        else:   return None

    def insert(self, code:str, char:str) -> bool:
        if len(code) > 1:
            if code[0] == '0' :
                if self.left == None: self.left = Node('')
                return self.left.insert(code[1:], char)
            elif code[0] == '1' :
                if self.right == None: self.right = Node('')
                return self.right.insert(code[1:], char)
            else: return False
        elif len(code) ==  1:
            if code[0] == '0' :
                if self.left == None: self.left = Node(char)
                return True
            elif code[0] == '1' :
                if self.right == None: self.right = Node(char)
                return True
            else: return False
        else: return False

def printNodes(node, val=''):
    """
    Utility function to print huffman
    codes for all symbols in the newly
    created Huffman tree
    """
    # Huffman code for current node
    newVal = val + str(node.huff)
    # if node is not an edge node
    # then traverse inside it
    if(node.left):
        printNodes(node.left, newVal)
    if(node.right):
        printNodes(node.right, newVal)
 
        # if node is edge node then
        # display its huffman code
    if(not node.left and not node.right):
        print(f"{ord(node.symbol)} \t-> {newVal}")

def getSymbolsCode(node, val='') -> list:
    """
    Utility function to get a list of huffman
    codes for all symbols in a Huffman tree.
    list of tuples (symbol, code)
    """
    # Huffman code for current node
    newVal = val + str(node.huff)
    codeList = []
    # if node is not an edge node
    # then traverse inside it
    if(node.left):
        codeList += getSymbolsCode(node.left, newVal)
    if(node.right):
        codeList += getSymbolsCode(node.right, newVal)
    # if node is edge node then
    # display its huffman code
    if(not node.left and not node.right):
        codeList.append((node.symbol, newVal))
    return codeList
