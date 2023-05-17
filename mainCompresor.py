import time

from burrows_wheeler import *
from tree_dataStruct import *
from ioFile import *

N_SYMBOLS = 256
BWT_LENGTH = 256
RBW_LENGTH = 257

def compress(file_path_source:str, file_path_destination:str):
    start_time = time.time()

    fileExtension = 'txt'

    #-- File -> Char String
    charString = readFileToCharString(file_path_source)

    # payLoad = Number of bytes of information.
    payload = len(charString)

    #-- Burrows Weelers
    # Split the file into nBlocks of size BWT_LENGTH.
    # If the last block is not of size BWT_LENGTH, fill it with chr(1)

    excessBytes = payload % BWT_LENGTH
    if excessBytes == 0: nBlock = len(charString) // BWT_LENGTH
    else:
        nBlock = (len(charString) // BWT_LENGTH) + 1
        charString += chr(0) * (256 - excessBytes)

    bwCharString = ''
    for offset in range(nBlock):
        bwCharString += bwt(charString[BWT_LENGTH*offset:BWT_LENGTH*(offset+1)])

    #print("- Burrows Weelers Transform Check")
    #print("--- %s seconds ---" % (time.time() - start_time))

    #-- Huffman - Markov Orden 1
    #-- based on https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/

    markovString = chr(0) + bwCharString

    # List containing Huffman Code Tree for all initial state.
    transitionMatrix = []
    huffmanTreeList = []

    # Converting characters and frequencies into huffman tree nodes.
    for i in range(N_SYMBOLS):
        # Nodes list sorted by freq.
        newTree = []
        newRowTransitionMatrix = []
        for j in range(N_SYMBOLS):
            newRowTransitionMatrix.append(markovString.count(chr(i)+chr(j)))
            newTree.append(nodeHuff(newRowTransitionMatrix[j], chr(j)))

        transitionMatrix.append(newRowTransitionMatrix)
        # Sort all the nodes in ascending order based on their frequency
        newTree.sort(key=lambda x: x.freq)
        # Creation of the hufman tree for the initial state Char(i)
        while len(newTree) > 1:
            # Take the 2 smallest nodes.
            left = newTree[0]
            right = newTree[1]
            newTree = newTree[2:]
            # Assign directional value to these nodes
            left.huff = 0
            right.huff = 1
            # Combine the 2 smallest nodes to create new node as their parent
            newNode = nodeHuff(left.freq+right.freq, left.symbol+right.symbol, left, right)
            # Searching for the newNode position.
            index = len(newTree)
            for k in range(len(newTree)):
                if(newTree[k].freq > newNode.freq):
                    index = k
                    break
            # Insert newNode into the sorted list
            if index == len(newTree):   newTree = newTree[:index] + [newNode]
            else:                       newTree = newTree[:index] + [newNode] + newTree[index:]
        # Insert newCodeTree into the huffman tree list
        huffmanTreeList.append(newTree[0])

    #print("- Huffman - Markov-1stOrd Check")
    #print("--- %s seconds ---" % (time.time() - start_time))

    #-- Codification Header
    huffmanCodeMatrix = []
    for i in range(N_SYMBOLS):
        newRowHuffmanCodeMatrix = []
        codeList = getSymbolsCode(huffmanTreeList[i])
        codeList.sort(key=lambda x: x[0])
        for j in range(N_SYMBOLS):
            if transitionMatrix[i][j] == 0 :newRowHuffmanCodeMatrix.append('')
            else: newRowHuffmanCodeMatrix.append(codeList[j][1])
        huffmanCodeMatrix.append(newRowHuffmanCodeMatrix)

    """
    CharCodes:
        > CharA         : Initial State.
        > CharB         : Final State.
        > Length        : Code length.
        > Code          : CharA-CharB transition code.
    """
    headerCodeMatrix = ''

    for charA in range(N_SYMBOLS):
        for charB in range(N_SYMBOLS):
            codeLength = len(huffmanCodeMatrix[charA][charB])
            headerCodeMatrix += bin(charA)[2:].zfill(8)
            headerCodeMatrix += bin(charB)[2:].zfill(8)
            headerCodeMatrix += bin(codeLength)[2:].zfill(5)
            headerCodeMatrix += huffmanCodeMatrix[charA][charB]

    #-- Normalize length of HeaderCodeMatrix to bytes. (Completed by 0)
    excessBits = len(headerCodeMatrix) % 8
    if excessBits == 0: lenHeaderCodeMatrix = len(headerCodeMatrix) // 8
    else:
        lenHeaderCodeMatrix = (len(headerCodeMatrix) // 8) + 1
        headerCodeMatrix += '0' * (8 - excessBits)
    #print("- Code header Check")
    #print("--- %s seconds ---" % (time.time() - start_time))

    #-- File Codification
    data = ''
    bwBlockProgressBar = int(len(bwCharString) / 29)
    charA = 0
    for nChar in range(len(bwCharString)):
        charB = ord(bwCharString[nChar])
        data += huffmanCodeMatrix[charA][charB]
        charA = charB

    data = bin(payload)[2:].zfill(32) + data

    #-- Normalize length of CompressData to bytes. (Completed by 0)
    excessBits = len(data) % 8
    if excessBits == 0: lenData = len(data) // 8
    else:
        lenData = (len(data) // 8) + 1
        data += '0' * (8 - excessBits)

    #print(f"- Code data Check [{completedTasks}]")
    #print("--- %s seconds ---" % (time.time() - start_time))

    headerSize = 4 + 4 + 4 + lenHeaderCodeMatrix
    fileSize = headerSize + lenData
    fileExtensionCode = ''.join(bin(ord(x))[2:].zfill(8) for x in fileExtension)

    compressData = bin(fileSize)[2:].zfill(32) + bin(headerSize)[2:].zfill(32) + fileExtensionCode.zfill(32) + headerCodeMatrix + data
    binaryCompressData = b''.join(int(x,2).to_bytes(1, byteorder='big') for x in [compressData[i:i+8]
                        for i in range(0,len(compressData), 8)
                        ]
            )


    file_to_save = file_path_destination
    compressFile = open(file_to_save,'wb')
    compressFile.write(binaryCompressData)
    compressFile.close()

    print(time.time() - start_time)
