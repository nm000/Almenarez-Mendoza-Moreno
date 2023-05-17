import sys
from mainDecompressor import decompress

file_path_source2 = sys.argv[1]
file_path_destination2 = 'descomprimido-elmejorprofesor.txt'
decompressTask = decompress(file_path_source2, file_path_destination2)
