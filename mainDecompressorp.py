import time
from mpi4py import MPI

from burrows_wheeler import *
from tree_dataStruct import *
from ioFile import *

N_SYMBOLS = 256
BWT_LENGTH = 256
RBW_LENGTH = 257

def decompress(file_path_source:str, file_path_destination:str):

    start_time = time.time()


    #-- File -> Char String
    bitString = readFileToBitString(file_path_source)

    #-- File Header
    fileSize = int(bitString[0:32],2)
    headerSize = int(bitString[32:64],2)
    fileExtension = (''.join(chr(int(x,2)) for x in [bitString[i:i+8] for i in range(64,96,8)])).replace(chr(0),'')

    #-- Read CharsCode and make Huffman Code Matrix
    codeMatrixData = bitString[96:headerSize*8]
    huffmanCodeMatrix = [['' for i in range(N_SYMBOLS)] for j in range(N_SYMBOLS)]
    offset = 0
    lenCodeMatrixData = len(codeMatrixData)

    while (offset + 21) < lenCodeMatrixData:
        charA = int(codeMatrixData[offset:offset+8],2)
        charB = int(codeMatrixData[offset+8:offset+16],2)
        codeLength = int(codeMatrixData[offset+16:offset+21],2)
        huffmanCodeMatrix[charA][charB] = codeMatrixData[offset+21:offset+21+codeLength]
        offset += 21 + codeLength

        #--------------------------------------------------#
    #print("--- %s seconds ---" % (time.time() - start_time))

    huffmanCodeTreeList = []
    for charA in range(256):
        newTree = Node('')
        for charB in range(256): newTree.insert(huffmanCodeMatrix[charA][charB], chr(charB))
        huffmanCodeTreeList.append(newTree)

    #print(f' Huffman Code Tree List Check')
    #print("--- %s seconds ---" % (time.time() - start_time))

    #-- Decompress
    compressedData = bitString[headerSize*8:fileSize*8]
    offset = 0
    payload = int(compressedData[offset:offset+32],2)
    if payload % 256 == 0 : nBlock = payload // BWT_LENGTH
    else: nBlock = (payload // BWT_LENGTH) + 1

    offset += 32
    bwCharString = ''
    node = huffmanCodeTreeList[0]
    lenCompressedData = len(compressedData)
    while offset < lenCompressedData:
        if len(bwCharString) == nBlock*RBW_LENGTH:
            break
        #--------------------------------------------------#
        node = node.next(compressedData[offset])
        if node == None :
            break
        if node.isLeaf() :
            bwCharString += node.data
            node = huffmanCodeTreeList[ord(node.data)]
        offset += 1
    #print(' Decode Check')
    #print("--- %s seconds ---" % (time.time() - start_time))

    #-- Reverse Burrows Weelers
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Split the data into blocks
    nBlock = len(bwCharString) // RBW_LENGTH
    block_size = nBlock // size
    start_index = rank * block_size * RBW_LENGTH
    end_index = (rank + 1) * block_size * RBW_LENGTH if rank != size - 1 else nBlock * RBW_LENGTH
    blocks = [bwCharString[start_index:end_index][i:i+RBW_LENGTH] for i in range(0, end_index - start_index, RBW_LENGTH)]

    # Apply RBW transformation on each block
    rbwCharString = ''
    for block in blocks:
        rbwCharString += rbw(block)

    # Combine the results from all processes
    rbwCharString = comm.gather(rbwCharString, root=0)

    if rank == 0:
        rbwCharString = ''.join(rbwCharString)
        #print(f"- Reverse Burrows Weelers Check")
        #print("--- %s seconds ---" % (time.time() - start_time))
        decompressedData = rbwCharString[:payload]

        binaryDecompressedData = b''.join(ord(x).to_bytes(1, byteorder='big') for x in decompressedData)

        file_to_save = file_path_destination
        decompressedFile = open(file_to_save,'wb')
        decompressedFile.write(binaryDecompressedData)
        decompressedFile.close()

        print(time.time() - start_time)
