La implementación consiste en la clase HashPerfecto que, creará la tabla hash. 
La clase cuenta con atributos y métodos para almacenar el genoma, dividirlo en k-mers, 
codificar esos mismos k-mers y al final almacenarlos en tabla, mediante hashing perfecto. 
Además existen funciones para el análisis experimental y el main para probar el código.

La clase HashPerfecto recibe un string como parámetro en su constructor, 
el string debe contener solo los siguientes caracteres: A, C, T, G
En caso contrario tirará una excepción.

- El código se compila usando g++, no requiere ninguna opción especial.

	$ g++ *.cpp -o nombre_del_ejecutable

- Al ejecutar el ejecutable aparecerán dos opciones:

	1: Ingreso de archivo
	2: Ingreso manual de string

	Ingresar 1 en la consola conlleva a tres opciones más:
	
		1: GCF_000820745.1_Polynesia_massiliensis_MS3_genomic.fna
		2: t.txt
		Ingresar número o nombre del archivo:
	
		Donde:
		Ingresar 1 abre el archivo del genoma.
		Ingresar 2 abre el archivo un t.txt (usado para testeo).
		Ingresar un nombre de archivo (ej: archivo.txt), abrirá dicho archivo.

	Esta etapa elimina de los archivos las líneas que contengan datos no pertenecientes al genoma en sí.
	Ej: >NZ_CCYG01000001.1 Clostridiaceae bacterium MS3, whole genome shotgun sequence

	Ingresar 2 en la consola permitirá ingresar un string.
	Ej: AGTGTGTGACACAC

- Luego se creará el HashPerfecto. 
  Crear el hash para el genoma de Polynesia massiliensis demora unos 20 segundos en nuestro caso.

- Finalmente aparecerá esto:

	Ingresar 15-mer a buscar, 0 para salir
	
	Esta etapa es un while(true) donde se pueden ingresar k-mers para buscar si están presentes en el genoma.
	Ej: GGGGGGGGGGGGGGG
	Ingresar un 0 termina el bucle while, lo que conlleva a la finalización del ejecutable.

