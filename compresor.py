import sys
from mainCompresor import compress

file_path_source = sys.argv[1]
file_path_destination = 'comprimido.elmejorprofesor'
compressTask = compress(file_path_source, file_path_destination)
