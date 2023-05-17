def readFileToCharString(filePath:str):
    string = ''
    with open(filePath,'rb') as file:
        while True:
            byte = file.read(1)
            if not byte:
                break
            string+=chr(int.from_bytes(byte, byteorder='big'))
    return string

def readFileToBitString(filePath:str):
    string = ''
    with open(filePath,'rb') as file:
        while True:
            byte = file.read(1)
            if not byte:
                break
            string+=bin(int.from_bytes(byte, byteorder='big'))[2:].zfill(8)
    return string   
