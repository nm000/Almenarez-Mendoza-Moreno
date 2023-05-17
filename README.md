# PC2_Compresor

Este proyecto contiene un compresor, un descompresor y un verificador de archivos.


ATENCIÓN: El proyecto cuenta con dos ramas, Master consiste en el proyecto base sin paralelismo, mientras que Paralelizado consiste en el proyecto Paralelizado mediante MPI4PY.


ATENCIÓN: El proceso de compresión y posterior descompresión de archivos puede tardar un poco, ya que el proyecto no usa ningún tipo de librería interna ni externa de Python para hacer cálculos y estructuras de datos. Tener paciencia.


Para ejecutar, es necesario contar con Python 3.19.
Una vez ubicado desde la terminal en el directorio del proyecto, puede ejecutar lo siguiente:


python compresor.py NombreArchivo, para comprimir el archivo. Este en caso de ser el proyecto sin paralelismo.
mpiexec -np <numberofproccesses> python3 compresorp.py. Este en caso de ser el proyecto paralelizado.


python descompresor.py, para descomprimir el archivo. Este en caso de ser el proyecto sin paralelismo.
mpiexec -np <numberofproccesses> python3 descompresorp.py. Este en caso de ser el proyecto paralelizado.


python verificador.py NombreArchivo, para comprobar si el archivo orignal y el descomprimido son el mismo. Este en caso de ser el proyecto sin paralelismo.
