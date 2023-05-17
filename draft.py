def bwt(inputStr:str) -> str:
    """
    Burrows-Wheeler-Transform
    """
    newRow = inputStr*2
    bwMatrix = []
    for i in range(len(inputStr)): bwMatrix.append(newRow[i:len(inputStr)+i])

    """
    Description of what's coming -.-'
    bwMatrix          = [2,3,1,4,5] -> Unsorted list
    sortedBwMatrix    = [1,2,3,4,5] -> Sorted list
    indexBwMatrix     = [2,0,1,3,4] -> Sorted list (by key) of unsorted list index *kill me*
    bwPosition        = 1           -> Index in sorted list of the first element in unsorted list
    """
    sortedBwMatrix = sorted(bwMatrix)
    indexBwMatrix  = sorted(range(len(bwMatrix)),key=lambda x: bwMatrix[x])
    bwPosition = indexBwMatrix.index(0)

    outputStr = chr(bwPosition)
    for row in sortedBwMatrix: outputStr += row[-1]
    return outputStr

def rbw(inputStr:str) -> str:
    """
    Reverse-Burrows-Wheeler
    """
    outputSelect = ord(inputStr[0])
    inputStr = inputStr[1:]
    bwMatrix = sorted(list(inputStr))
    for i in range(len(inputStr)-1):
        for j in range(len(inputStr)):
            bwMatrix[j]=inputStr[j]+bwMatrix[j]
        bwMatrix.sort()
    return bwMatrix[outputSelect]

def testBurrowsWeeler():
    testString = 'PABLOPABLITOCLAVOUNCLAVITO'
    print('-'*50)
    print(' > Test String = '+ testString)
    bwtString = bwt(testString)
    print(' > BWT String  = '+ bwtString)
    rbwString = rbw(bwtString)
    print(' > RBW String  = '+ rbwString)
    print('-'*50)

def testBinary():
    fileName = 'background.png'
    file_path = f'fileTest\{fileName}'
    inputFile = open(rf'fileTest\{fileName}','rb')
    bytesString = inputFile.read()
    print(bytesString)
    print('-'*50)
    # charString = ''.join(int.from_bytes(bytes, byteorder='big') for byte in bytesString)
    charString = bytesString.decode
    print(charString)
    print('-'*50)

def testHeader():
    # listA = [('A',1),('B',2)]
    # listB = [('C',3)]
    # listC = []
    # listC += listA
    # listC += listB

    # listA = [['']*3]*3
    # listA = [['','',''],['','',''],['','','']]
    listA = [['' for j in range(3)] for i in range(3)]
    listA[1][2] = 'a'

    print(listA)
    print(listA[1])

if __name__ == "__main__":
    testHeader()
