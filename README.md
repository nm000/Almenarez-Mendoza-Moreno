#PC2_Compressor

Este proyecto contiene un compresor secuencial y paralelizado, un descompresor secuencial y paralelizado y un verificador de archivos. Adicionalmente, se tienen distintos archivos .py que soportan la lógica de la compresión y descompresión de manera más ordenada.

ATENCIÓN: El proceso de compresión y posterior descompresión de archivos puede tardar un poco, ya que el proyecto no usa ningún tipo de librería interna ni externa de Python para hacer cálculos y estructuras de datos. Tener paciencia.

Para ejecutar, es necesario contar con Python 3.19. Una vez ubicado desde la terminal en el directorio del proyecto, puede ejecutar lo siguiente:

python compresor.py NombreArchivo, para comprimir el archivo. Este en caso de ser el proyecto sin paralelismo. 
mpiexec -np python3 compresorp.py. Este en caso de ser el proyecto paralelizado.

python descompresor.py, para descomprimir el archivo. Este en caso de ser el proyecto secuencial
mpiexec -np python3 descompresorp.py. Este en caso de ser el proyecto paralelizado.

python verificador.py NombreArchivo1 NombreArchivo2, para comprobar si el archivo orignal y el descomprimido son el mismo. Este funciona tanto para la versión secuencial, como paralelizada.
